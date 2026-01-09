---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication & Authorization Skill

## Instructions

1. **User Registration (Signup)**
   - Validate user input (email, password, username)
   - Enforce strong password rules
   - Prevent duplicate accounts
   - Store users securely in the database

2. **User Login (SignIn)**
   - Authenticate users using email/username and password
   - Compare hashed passwords securely
   - Handle invalid credentials gracefully
   - Implement rate limiting to prevent brute-force attacks

3. **Password Hashing**
   - Use industry-standard hashing algorithms (e.g., bcrypt, argon2)
   - Apply proper salting
   - Never store plain-text passwords
   - Support password reset and update flows

4. **JWT Token Management**
   - Generate access tokens on successful authentication
   - Include minimal, non-sensitive payload data
   - Set appropriate expiration times
   - Verify and decode tokens for protected routes
   - Implement refresh tokens if required

5. **Better Auth Integration**
   - Configure Better Auth provider
   - Integrate with existing user models
   - Support session-based and token-based authentication
   - Enable social login or external providers if needed

## Security Best Practices
- Use HTTPS everywhere
- Store secrets and keys in environment variables
- Rotate JWT secrets periodically
- Implement proper error handling without leaking sensitive details
- Follow OWASP authentication guidelines

## Example Structure
```ts
// Signup
app.post("/signup", async (req, res) => {
  const { email, password } = req.body;
  const hashedPassword = await bcrypt.hash(password, 12);
  // save user to database
});

// SignIn
app.post("/signin", async (req, res) => {
  const user = await findUser(req.body.email);
  const isValid = await bcrypt.compare(req.body.password, user.password);
  if (!isValid) return res.status(401).send("Invalid credentials");

  const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, {
    expiresIn: "1h",
  });

  res.json({ token });
});

// Protected Route
app.get("/profile", authenticateJWT, (req, res) => {
  res.json({ user: req.user });
});
