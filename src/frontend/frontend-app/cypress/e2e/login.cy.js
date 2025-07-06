describe('Login Flow', () => {
  it('should successfully log in a user', () => {
    cy.visit('http://localhost:5173'); // Assuming your Vite app runs on port 5173

    // Type in username and password
    cy.get('input[name=username]').type('testuser');
    cy.get('input[name=password]').type('testpass');

    // Click the login button
    cy.get('button[type=submit]').click();

    // Assert that the user is redirected to the dashboard or a protected route
    // This will depend on your application's routing after successful login
    cy.url().should('include', '/agent-management'); // Example: check for dashboard URL
    cy.contains('Agent Management'); // Example: check for content on the dashboard
  });

  it('should display an error message for invalid credentials', () => {
    cy.visit('http://localhost:5173');

    // Type in invalid username and password
    cy.get('input[name=username]').type('wronguser');
    cy.get('input[name=password]').type('wrongpass');

    // Click the login button
    cy.get('button[type=submit]').click();

    // Assert that an error message is displayed
    cy.contains('Invalid credentials').should('be.visible');
  });
});