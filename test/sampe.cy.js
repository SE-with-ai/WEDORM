describe('Test model', () => {
    it('phrase1', () => {
        cy.visit({url: 'home.html'})
        cy.contains('Home').click()
        cy.contains('Login').click()
        cy.get('[id=login]').within(() =>{
          cy.get('[placeholder="Enter Username"]').type('Als')
          cy.get('[placeholder="Enter Password"]').type('Als')
          cy.get('[class=close]').click()
        })

        cy.contains('Register').click()
        cy.get('[id=register]').within(() =>{
          cy.get('[placeholder="Enter Username"]').type('Als')
          cy.get('[placeholder="Enter Password"]').type('Als')
          cy.get('[placeholder="Enter Email"]').type('Als@Als')
          cy.get('[placeholder="Enter Student Number"]').type('1123')
        })
        //cy.get('[#login,placeholder="Enter Username"]')
    })
  })