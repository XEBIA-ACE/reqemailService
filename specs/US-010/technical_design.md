## SRV003

### 1. Contracts & Interfaces

#### 1.1 REST API Contracts

- **POST /api/v1/emails/validate**
  - Purpose: Validate a single email address for registration, providing actionable feedback.
  - Request Payload: 
    - `email_address: string` (REQUIRED)
  - Response 200 (Valid Email):
    - `field_name: "email_address"`
    - `is_valid: true`
    - `error_message: ""`
  - Response 400 (Invalid Email):
    - `field_name: "email_address"`
    - `is_valid: false`
    - `error_message: "<human-readable description>"`
    - `error_code: "<error code, e.g. EMAIL_REQUIRED|INVALID_FORMAT>"`
  - Response 400 (Missing Email):
    - `field_name: "email_address"`
    - `is_valid: false`
    - `error_message: "Email is required"`
    - `error_code: "EMAIL_REQUIRED"`
  - Response 429 (optional): If rate-limiting validation attempts (out of scope for base FRs, see A-005).

- **PATCH /api/v1/emails/verification**
  - Description: Modified to accept only valid requests post-validation.
  - Change: Documentation MUST indicate that email_address is validated; rejected with HTTP 400 and error response if validation fails.

#### 1.2 Data Schemas

- **ValidationFeedback**
  - `field_name: string`
  - `is_valid: boolean`
  - `error_message: string`
  - `error_code: string`

#### 1.3 Interfaces

- **IEmailValidator**
  - `validate(email_address: str) -> ValidationFeedback`

---

### 2. Test Strategy

#### 2.1 Endpoint Contract Tests

- **Test: Valid Email Address**
  - Endpoint: POST /api/v1/emails/validate
  - Input: { "email_address": "user@example.com" }
  - Expect: `is_valid` = true, `error_message` = "", HTTP 200

- **Test: Missing Email Address**
  - Endpoint: POST /api/v1/emails/validate
  - Input: { }
  - Expect: `is_valid` = false, `field_name` = "email_address", `error_code` = "EMAIL_REQUIRED", `error_message` = "Email is required", HTTP 400

- **Test: Invalid Email Structure**
  - Input: { "email_address": "user@" }
  - Expect: `is_valid` = false, `field_name` = "email_address", `error_code` = "INVALID_FORMAT", `error_message` = "Invalid email address", HTTP 400

- **Test: Blank Email Field**
  - Input: { "email_address": "" }
  - Expect: `is_valid` = false, HTTP 400, error message "Email is required"

- **Test: PATCH /api/v1/emails/verification with invalid email**
  - Input: { "email_address": "bademail@" }
  - Expect: HTTP 400, error message "Invalid email address"

- **Test: Success Feedback on Correction**
  - Input (after previous failure): { "email_address": "good@mail.com" }
  - Expect: `is_valid` = true, HTTP 200

#### 2.2 Edge Case Tests

- EC-001, EC-003, EC-004, EC-005, EC-007 covered in above contract tests.

#### 2.3 Logging (Optional/Conditional)

- **Test: Excessive invalid attempts**
  - Simulate repeated invalid requests.
  - Expect: Entry in validation_error_log table or analytics stream (if implemented).

---

### 3. Implementation Approach

#### 3.1 Core Components

- **EmailValidator (class/module)**
  - Method: `validate(email_address: str) -> ValidationFeedback`
    - Uses RFC 5322 regex for format, and checks non-blank.
  - Returns a ValidationFeedback instance according to business rules in A-001 and A-002.

- **ValidationFeedback (model/class)**
  - Implements schema above.

- **API Handler**
  - Node.js: `EmailValidationController.validateEmail(req, res)`
  - Django REST: `EmailValidationAPIView.post(self, request)`

#### 3.2 Endpoint Integration

- **/api/v1/emails/validate**
  - New endpoint in api_handler component.
  - Calls `EmailValidator.validate`.
  - On invalid, responds HTTP 400, see contract.
  - On valid, responds HTTP 200, see contract.

- **/api/v1/emails/verification**
  - On receipt, invokes EmailValidator for email_address before ANY verification send logic.
  - If invalid, returns HTTP 400, field-level errors, stops further processing per FR-004, FR-005.

#### 3.3 Data Model Changes

- **No persistent user data** per A-006 and functional scope.
- **Optional table**: validation_error_log
  - Columns: id (PK), email_address, error_code, created_at (if logging enabled, per FR-008).

#### 3.4 Async & Inter-service Calls

- **No external calls required** (A-004).
- No background processing or queuing needed for validation.

#### 3.5 Error Messaging

- Error message templates localized in code.
- Only field-level (not form summary) feedback returned.

---

### ADRs

#### ADR-001: Standard REST Validation Endpoint Pattern for User Input
- **Context**: Requirement for explicit, reusable validation feedback for registration forms.
- **Decision**: Adopt a REST POST endpoint (/api/v1/emails/validate) with decoupled input