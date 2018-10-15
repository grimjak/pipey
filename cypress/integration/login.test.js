describe('Login', () => {
    it('should display the sign in form', () => {
        cy
            .visit('/login')
            .get('h1').contains('login')
            .get('form')
            .get('input[disabled]')
            .get('.validation-list')
            .get('.validation-list > .error').first().contains(
                'Username is required');
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
        cy.get('.notification.is-success').contains('Welcome!');
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
    it('should throw an error if the credentials are incorrect', () => {
        // bad username
        cy
            .visit('/login')
            .get('input[name="username"]').type('badUser')
            .get('input[name="password"]').type('greaterthaneight')
            .get('input[type="submit"]').click()
            .wait(300);

        // cy.contains('All Users').should('.not.be.visible');
        cy.contains('login');
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('User Status').should('.not.be.visible')
                .get('.navbar-item').contains('Log Out').should('.not.be.visible')
                .get('.navbar-item').contains('Log In');
        });
        cy
            .get('.notification.is-success').should('not.be.visible')
            .get('.notification.is-danger').contains('User does not exist.');
        
        //bad password
        cy
            .get('a').contains('Log In').click()
            .get('input[name="username"]').type('tb')
            .get('input[name="password"]').type('badPassword')
            .get('input[type="submit"]').click()
            .wait(100);

        cy.contains('All Users').should('.not.be.visible');
        cy.contains('login');
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('User Status').should('.not.be.visible')
                .get('.navbar-item').contains('Log Out').should('.not.be.visible')
                .get('.navbar-item').contains('Log In');
        });
        cy
            .get('.notification.is-success').should('not.be.visible')
            .get('.notification.is-danger').contains('User does not exist.');
    });
});