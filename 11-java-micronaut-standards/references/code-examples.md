# ☕ Micronaut 4+ Reference Implementations

Exemplos canônicos de código para Micronaut 4+ e Java 21+, demonstrando injeção Ahead-of-Time (AOT), prevenção de N+1 com `@Join`, DTOs com Java Records e testes com `@MicronautTest`.

---

## 1. Controller Reference (`AssetController.java`)

```java
package com.portfolio.fleet.controller;

import com.portfolio.fleet.dto.AssetDTO;
import com.portfolio.fleet.dto.CreateVehicleRequest;
import com.portfolio.fleet.dto.VehicleDTO;
import com.portfolio.fleet.service.AssetService;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.*;
import io.micronaut.scheduling.TaskExecutors;
import io.micronaut.scheduling.annotation.ExecuteOn;
import jakarta.validation.Valid;

@Controller("/api/assets")
@ExecuteOn(TaskExecutors.BLOCKING)
public class AssetController {

    private final AssetService assetService;

    public AssetController(AssetService assetService) {
        this.assetService = assetService;
    }

    @Post("/vehicles")
    public HttpResponse<VehicleDTO> registerVehicle(@Valid @Body CreateVehicleRequest request) {
        VehicleDTO created = assetService.create(request);
        return HttpResponse.created(created);
    }

    @Get("/{id}")
    public HttpResponse<AssetDTO> getById(@PathVariable Long id) {
        return assetService.findById(id)
            .map(HttpResponse::ok)
            .orElseGet(HttpResponse::notFound);
    }
}
```

---

## 2. Repository Reference (`AssetRepository.java`)

```java
package com.portfolio.fleet.repository;

import com.portfolio.fleet.dto.AssetSummaryDTO;
import com.portfolio.fleet.entity.Asset;
import com.portfolio.fleet.model.AssetStatus;
import io.micronaut.data.annotation.Join;
import io.micronaut.data.annotation.Query;
import io.micronaut.data.annotation.Repository;
import io.micronaut.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.Optional;

@Repository
public interface AssetRepository extends JpaRepository<Asset, Long> {

    // Prevents N+1 by forcing compile-time INNER JOIN FETCH
    @Join(value = "operator", type = Join.Type.FETCH)
    @Join(value = "maintenanceSchedules", type = Join.Type.LEFT_FETCH)
    Optional<Asset> findWithDetailsById(Long id);

    // Constructor-expression projection with Java text blocks
    @Query("""
        SELECT new com.portfolio.fleet.dto.AssetSummaryDTO(
            a.id, a.assetCode, a.name, a.status, o.name
        )
        FROM Asset a
        LEFT JOIN a.operator o
        WHERE a.status = :status
    """)
    List<AssetSummaryDTO> findSummariesByStatus(AssetStatus status);
}
```

---

## 3. Test Reference (`AssetControllerTest.java`)

```java
package com.portfolio.fleet.controller;

import com.portfolio.fleet.dto.CreateVehicleRequest;
import com.portfolio.fleet.dto.VehicleDTO;
import io.micronaut.http.HttpRequest;
import io.micronaut.http.HttpStatus;
import io.micronaut.http.client.HttpClient;
import io.micronaut.http.client.annotation.Client;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

@MicronautTest
class AssetControllerTest {

    @Inject
    @Client("/api/assets")
    HttpClient client;

    @Test
    void should_ReturnCreated_When_VehicleRequestIsValid() {
        var request = HttpRequest.POST("/vehicles", new CreateVehicleRequest("TRK-01", "Volvo FH"));
        var response = client.toBlocking().exchange(request, VehicleDTO.class);

        assertThat(response.getStatus()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.body()).isNotNull();
        assertThat(response.body().assetCode()).isEqualTo("TRK-01");
    }
}
```
