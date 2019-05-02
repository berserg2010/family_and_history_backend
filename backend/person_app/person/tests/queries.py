# PERSON
ALL_PERSON = '''
query AllPerson{
    allPerson{
        id        
    }
}
'''

PERSON = '''
query Person($id: ID!){
    person(id: $id){
        id
    }
}
'''

SAVE_PERSON = '''
mutation CreatePerson(
    $data: PersonInput
){
    savePerson(
        data: $data
    ){
        status
        formErrors
        person{
            id
        }
    }
}
'''

DELETE_PERSON = '''
mutation DeletePerson($id: ID!){
    deletePerson(id: $id){
        status
        id
    }
}
'''

SEARCH_PERSON = '''
query SearchPerson($searchTerm: String){
    searchPerson(searchTerm: $searchTerm){
        id
        birth{
            surname
        }
    }
}
'''
