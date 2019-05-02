# FAMILY
ALL_FAMILY = '''
query AllFamily{
    allFamily{
        id        
    }
}
'''

FAMILY = '''
query Family($id: ID!){
    family(id: $id){
        id
    }
}
'''

SAVE_FAMILY = '''
mutation CreateFamily(
    $data: FamilyInput
){
    saveFamily(
        data: $data
    ){
        status
        formErrors
        family{
            id
        }
    }
}
'''

DELETE_FAMILY = '''
mutation DeleteFamily($id: ID!){
    deleteFamily(id: $id){
        status
        id
    }
}
'''

# CHILD
ALL_CHILD = '''
query AllChild($idFamily: ID){
    allChild(idFamily: $idFamily){
        id        
    }
}
'''

CHILD = '''
query Child($id: ID!){
    child(id: $id){
        id
    }
}
'''

SAVE_CHILD = '''
mutation CreateChild(
    $data: ChildInput
){
    saveChild(
        data: $data
    ){
        status
        formErrors
        child{
            id
        }
    }
}
'''

DELETE_CHILD = '''
mutation DeleteChild($id: ID!){
    deleteChild(id: $id){
        status
        id
    }
}
'''
