describe('Login', () => {
    it('should display the sign in form', () => {
        cy
            .visit('login')
            .get('h1').contains('login')
            .get('form');
    });
    it('should allow a user to sign in', () => {
        //make sure we have a registered user
        cy.get('.navbar-burger').click()
        cy
            .get('a').contains('Log in').click()
            .get('input[name="username"]').type('tb')
            .get('input[name="password"]').type('greaterthaneight')
            .get('input[type="submit"]').click()
            .wait(400);

        //assert user is redirected to '/'
        //assert '/' is displayed properly
        cy.contains('All Users');
        cy
            .get('table')
            .find('tbody > tr').last()
            .find('td').contains('bh');
        cy.get('.navbar-burger').click();
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('User Status')
                .get('.navbar-item').contains('Log out')
                .get('.navbar-item').contains('Log in').should('not.be.visible')
        });

        //log a user out
        cy.get('.navbar-burger').click()
        cy
            .get('a').contains('Log out').click();

        // assert '/logout is displayed properly
        cy.get('p').contains('You are now logged out');
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('User Status').should('not.be.visible')
                .get('.navbar-item').contains('Log out').should('not.be.visible')
                .get('.navbar-item').contains('Log in');
        });
    })
});