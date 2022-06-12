import uuid
from ts.services.contacts_service import (
    gen_random_contact,
    get_all_contacts_request,
    add_one_contact_request,
    delete_one_contact_request,
    update_one_contact_request,
    restore_original_contacts,
    ORIGINAL_CONTACTS,
)


def test_all(request_id, admin_bearer, assertIsInstance, assertEqual):
    _test_gen_random_contact()
    _test_get_all_contacts_request(request_id, admin_bearer, assertIsInstance)
    _test_add_one_contact_request(request_id, admin_bearer)
    _test_update_one_contact_request(request_id, admin_bearer, assertEqual)
    _test_delete_one_contact_request(request_id, admin_bearer, assertEqual)
    # _test_restore_original_contacts(request_id, admin_bearer, assertEqual)


def _test_gen_random_contact():
    print("Test gen_random_contact")
    print(gen_random_contact(str(uuid.uuid4()), str(uuid.uuid4())).__dict__)


def _test_get_all_contacts_request(
    request_id: str, admin_bearer: str, assertIsInstance
):
    print("Test get_all_contacts_request")
    contacts = get_all_contacts_request(request_id, admin_bearer)
    print(contacts[:10])
    assertIsInstance(contacts, list)


def _test_add_one_contact_request(request_id: str, admin_bearer: str):
    print("Test add_one_contact_request")
    new_contact = gen_random_contact(None, "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f")
    added_contact = add_one_contact_request(request_id, admin_bearer, new_contact)
    print(added_contact)


def _test_update_one_contact_request(request_id: str, admin_bearer: str, assertEqual):
    print("Test update_one_contact_request")
    contacts = get_all_contacts_request(request_id, admin_bearer)
    contact = contacts[-1]
    new_contact = gen_random_contact(contact["id"], contact["accountId"])
    updated_contact = update_one_contact_request(request_id, admin_bearer, new_contact)
    assertEqual(updated_contact["id"], new_contact.id)
    assertEqual(updated_contact["accountId"], new_contact.user_id)
    assertEqual(updated_contact["name"], new_contact.name)
    assertEqual(updated_contact["documentType"], new_contact.document_type)
    assertEqual(updated_contact["documentNumber"], new_contact.document_number)
    assertEqual(updated_contact["phoneNumber"], new_contact.phone_number)


def _test_delete_one_contact_request(request_id: str, admin_bearer: str, assertEqual):
    print("Test delete_one_contact_request")
    contacts = get_all_contacts_request(request_id, admin_bearer)
    contact_id = contacts[-1]["id"]
    deleted_contact_id = delete_one_contact_request(
        request_id, admin_bearer, contact_id
    )
    print(deleted_contact_id)
    assertEqual(deleted_contact_id, contact_id)


# def _test_restore_original_contacts(request_id: str, admin_bearer: str, assertEqual):
#     print("Test restore_original_contacts")
#     restore_original_contacts(request_id, admin_bearer)
#     contacts = get_all_contacts_request(request_id, admin_bearer)
#     assertEqual(contacts, ORIGINAL_CONTACTS)
