
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
            .get('.notification.is-success').should('not.be.visible')
            .get('.notification.is-danger').contains('User does not exist.')
            .get('.delete').click()
            .get('.notification.is-danger').should('not.be.visible');

        cy
            .get('input[name="username"]').type('tb')
            .get('input[name="password"]').type('greaterthaneight')
            .get('input[type="submit"]').click()
            .wait(100);

        cy
            .get('.notification.is-success').contains('Welcome!')
            .get('.notification.is-danger').should('not.be.visible')
            .wait(4000)
            .get('.notification.is-success').should('not.be.visible');      
    })

})