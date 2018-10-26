describe('Status', () => {
    it('should not display user info if a user is not logged in', () => {
        cy
            .visit('/status')
            .get('p').contains('You must be logged in to view this.')
            .get('a').contains('User Status').should('not.be.visible')
            .get('a').contains('Log out').should('not.be.visible')
            .get('a').contains('Log in');
    });
    it('should display user info if a user is logged in', () => {
        //make sure we have a registered user
        cy.get('.navbar-burger').click()
        cy
            .get('a').contains('Log in').click()
            .get('input[name="username"]').type('tb')
            .get('input[name="password"]').type('greaterthaneight')
            .get('input[type="submit"]').click()
            .wait(400);

        cy.visit('/status');
        //cy.get('.navbar-burger').click();
        //cy.contains('User Status').click();
        cy.get('li > strong').contains('User ID:')
            .get('li > strong').contains('username:')
            .get('li').contains('tb')

    })
})