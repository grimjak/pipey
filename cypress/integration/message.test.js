
describe('Message', () => {

    it(`should display flash messages correctly`, () => {
        // bad username
        cy
            .visit('/login')
            .get('input[name="username"]').type('badUser')
            .get('input[name="password"]').type('greaterthaneight')
            .get('input[type="submit"]').click()
            .wait(100);

        cy
            .get('.notification.is-success').should('not.exist');
        cy
            .get('.notification.is-danger').contains('User does not exist.')
            .get('.delete').click();
        cy
            .get('.notification.is-danger').should('not.exist');

        cy
            .visit('/login')
            .get('input[name="username"]').type('tb')
            .get('input[name="password"]').type('greaterthaneight')
            .get('input[type="submit"]').click()
            .wait(100);

        cy
            .get('.notification.is-success').contains('Welcome!');
        
        cy
            .get('.notification.is-danger').should('not.exist')
            .wait(4000);
        cy
            .get('.notification.is-success').should('not.exist');   
    })

})