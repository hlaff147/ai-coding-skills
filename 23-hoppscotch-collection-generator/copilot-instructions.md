# Hoppscotch Collection & Test Generator (GitHub Copilot)

When generating Hoppscotch collections, environments, or API test scripts:

1. **Variable Interpolation**:
   - Use double angle brackets `<<variable_name>>` for environment variables, never Postman's `{{variable_name}}`.

2. **Test Scripts (`pw.*`)**:
   - Write tests using Hoppscotch's native `pw` global object:
     - `pw.expect(pw.response.status).toBe(200);`
     - `pw.env.set("token", JSON.parse(pw.response.body).token);`
   - Never use `pm.*`.

3. **Collection Schema**:
   - Output valid Hoppscotch v2 collection JSON with `name`, `folders`, and `requests` arrays.
