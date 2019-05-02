# BIRTH
ALL_BIRTH = '''
query AllBirth($idPerson: ID){
    allBirth(idPerson: $idPerson){
        id
    }
}
'''

BIRTH = '''
query Birth($id: ID!){
    birth(id: $id){
        id
    }
}
'''

SAVE_BIRTH = '''
mutation SaveBirth(
    $data: BirthInput
){
    saveBirth(
        data: $data
    ){
        status
        formErrors
        birth{
            id
        }
    }
}
'''

DELETE_BIRTH = '''
mutation DeleteBirth($id: ID!){
    deleteBirth(id: $id){
        status
        id
    }
}
'''

SEARCH_BIRTH = '''
query SearchBirth($searchTerm: String){
    searchBirth(searchTerm: $searchTerm){
        id
        surname
    }
}
'''

LIKE_BIRTH = '''
mutation LikeBirth($id: ID!, $email: String!){
    likeBirth(
        id: $id,
        email: $email,
    ){
        birth{
            likes
        }
    }
}
'''
