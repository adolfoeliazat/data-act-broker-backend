import json
import pytest
from unittest.mock import Mock

from dataactbroker.handlers import accountHandler
from dataactcore.models.lookups import PERMISSION_TYPE_DICT, PERMISSION_SHORT_DICT
from dataactcore.models.userModel import UserAffiliation
from dataactcore.utils.jsonResponse import JsonResponse
from dataactcore.utils.statusCode import StatusCode
from tests.unit.dataactcore.factories.domain import CGACFactory, FRECFactory
from tests.unit.dataactcore.factories.user import UserFactory


def make_max_dict(group_str):
    """We need to create mock MAX data at multiple points in these tests"""
    return {
        'cas:serviceResponse': {
            'cas:authenticationSuccess': {
                'cas:attributes': {
                    'maxAttribute:Email-Address': 'test-user@email.com',
                    'maxAttribute:GroupList': group_str,
                    'maxAttribute:First-Name': 'test',
                    'maxAttribute:Middle-Name': '',
                    'maxAttribute:Last-Name': 'user'
                }
            }
        }
    }


@pytest.mark.usefixtures("user_constants")
def test_max_login_success(monkeypatch):
    ah = accountHandler.AccountHandler(Mock())

    mock_dict = Mock()
    mock_dict.return_value.safeDictionary.side_effect = {'ticket': '', 'service': ''}
    monkeypatch.setattr(accountHandler, 'RequestDictionary', mock_dict)

    max_dict = {'cas:serviceResponse': {}}
    monkeypatch.setattr(accountHandler, 'get_max_dict', Mock(return_value=max_dict))
    config = {'parent_group': 'parent-group'}
    monkeypatch.setattr(accountHandler, 'CONFIG_BROKER', config)
    max_dict = make_max_dict('parent-group,parent-group-CGAC_SYS')
    monkeypatch.setattr(accountHandler, 'get_max_dict', Mock(return_value=max_dict))

    # If it gets to this point, that means the user was in all the right groups aka successful login
    monkeypatch.setattr(ah, 'create_session_and_response',
                        Mock(return_value=JsonResponse.create(StatusCode.OK, {"message": "Login successful"})))
    json_response = ah.max_login(Mock())

    assert "Login successful" == json.loads(json_response.get_data().decode("utf-8"))['message']

    max_dict = make_max_dict('')
    monkeypatch.setattr(accountHandler, 'get_max_dict', Mock(return_value=max_dict))

    # If it gets to this point, that means the user was in all the right groups aka successful login
    monkeypatch.setattr(ah, 'create_session_and_response',
                        Mock(return_value=JsonResponse.create(StatusCode.OK, {"message": "Login successful"})))
    json_response = ah.max_login(Mock())

    assert "Login successful" == json.loads(json_response.get_data().decode("utf-8"))['message']


def test_max_login_failure(monkeypatch):
    ah = accountHandler.AccountHandler(Mock())
    config = {'parent_group': 'parent-group'}
    monkeypatch.setattr(accountHandler, 'CONFIG_BROKER', config)

    mock_dict = Mock()
    mock_dict.return_value.safeDictionary.side_effect = {'ticket': '', 'service': ''}
    monkeypatch.setattr(accountHandler, 'RequestDictionary', mock_dict)

    max_dict = {'cas:serviceResponse': {}}
    monkeypatch.setattr(accountHandler, 'get_max_dict', Mock(return_value=max_dict))
    json_response = ah.max_login(Mock())
    error_message = "You have failed to login successfully with MAX"

    # Did not get a successful response from MAX
    assert error_message == json.loads(json_response.get_data().decode("utf-8"))['message']


@pytest.mark.usefixtures("user_constants")
def test_set_max_perms(database, monkeypatch):
    """Verify that we get the _highest_ permission within our CGAC"""
    cgac_abc = CGACFactory(cgac_code='ABC')
    cgac_def = CGACFactory(cgac_code='DEF')
    frec_abc = FRECFactory(frec_code='ABC', cgac=cgac_abc)
    frec_def = FRECFactory(frec_code='DEF', cgac=cgac_def)
    user = UserFactory()
    database.session.add_all([cgac_abc, cgac_def, frec_abc, frec_def, user])
    database.session.commit()

    monkeypatch.setitem(accountHandler.CONFIG_BROKER, 'parent_group', 'prefix')

    # create permission from permission string
    accountHandler.set_max_perms(user, 'prefix-CGAC_ABC-PERM_W')
    database.session.commit()   # populate ids
    assert len(user.affiliations) == 1
    affil = user.affiliations[0]
    assert affil.cgac_id == cgac_abc.cgac_id
    assert affil.permission_type_id == PERMISSION_TYPE_DICT['writer']

    # only highest CGAC permission type from multiple permission strings
    accountHandler.set_max_perms(user, 'prefix-CGAC_ABC-PERM_R,prefix-CGAC_ABC-PERM_S')
    database.session.commit()   # populate ids
    assert len(user.affiliations) == 1
    affil = user.affiliations[0]
    assert affil.cgac_id == cgac_abc.cgac_id
    assert affil.permission_type_id == PERMISSION_TYPE_DICT['submitter']

    # two separate CGAC permissions for separate CGACs
    accountHandler.set_max_perms(user, 'prefix-CGAC_ABC-PERM_R,prefix-CGAC_DEF-PERM_S')
    database.session.commit()   # populate ids
    assert len(user.affiliations) == 2
    affiliations = list(sorted(user.affiliations, key=lambda a: a.cgac.cgac_code))
    abc_aff, def_aff = affiliations
    assert abc_aff.cgac.cgac_code == 'ABC'
    assert abc_aff.frec is None
    assert abc_aff.permission_type_id == PERMISSION_TYPE_DICT['reader']
    assert def_aff.cgac.cgac_code == 'DEF'
    assert def_aff.frec is None
    assert def_aff.permission_type_id == PERMISSION_TYPE_DICT['submitter']

    # only highest FREC permission type from multiple permission strings, extra readonly CGAC for historical data
    accountHandler.set_max_perms(user, 'prefix-CGAC_ABC-FREC_ABC-PERM_R,prefix-CGAC_ABC-FREC_ABC-PERM_S')
    database.session.commit()   # populate ids
    assert len(user.affiliations) == 2
    frec_affils = [affil for affil in user.affiliations if affil.frec is not None]
    assert len(frec_affils) == 1
    assert frec_affils[0].cgac is None
    assert frec_affils[0].frec.frec_code == 'ABC'
    assert frec_affils[0].permission_type_id == PERMISSION_TYPE_DICT['submitter']
    cgac_affils = [affil for affil in user.affiliations if affil.cgac is not None]
    assert len(cgac_affils) == 1
    assert cgac_affils[0].cgac.cgac_code == 'ABC'
    assert cgac_affils[0].frec is None
    assert cgac_affils[0].permission_type_id == PERMISSION_TYPE_DICT['reader']

    # two separate FREC permissions for separate FRECs, extra readonly CGAC for historical data
    accountHandler.set_max_perms(user, 'prefix-CGAC_ABC-FREC_ABC-PERM_R,prefix-CGAC_ABC-FREC_DEF-PERM_S')
    database.session.commit()   # populate ids
    assert len(user.affiliations) == 3
    frec_affils = [affil for affil in user.affiliations if affil.frec is not None]
    assert len(frec_affils) == 2
    abc_aff, def_aff = list(sorted(frec_affils, key=lambda a: a.frec.frec_code))
    assert abc_aff.cgac is None
    assert abc_aff.frec.frec_code == 'ABC'
    assert abc_aff.permission_type_id == PERMISSION_TYPE_DICT['reader']
    assert def_aff.cgac is None
    assert def_aff.frec.frec_code == 'DEF'
    assert def_aff.permission_type_id == PERMISSION_TYPE_DICT['submitter']
    cgac_affils = [affil for affil in user.affiliations if affil.cgac is not None]
    assert len(cgac_affils) == 1
    assert cgac_affils[0].cgac.cgac_code == 'ABC'
    assert cgac_affils[0].frec is None
    assert cgac_affils[0].permission_type_id == PERMISSION_TYPE_DICT['reader']

    # one CGAC and one FREC, extra readonly CGAC for historical data
    accountHandler.set_max_perms(user, 'prefix-CGAC_ABC-PERM_S,prefix-CGAC_DEF-FREC_DEF-PERM_R')
    database.session.commit()   # populate ids
    assert len(user.affiliations) == 3
    frec_affils = [affil for affil in user.affiliations if affil.frec is not None]
    assert len(frec_affils) == 1
    assert frec_affils[0].cgac is None
    assert frec_affils[0].frec.frec_code == 'DEF'
    assert frec_affils[0].permission_type_id == PERMISSION_TYPE_DICT['reader']
    cgac_affils = [affil for affil in user.affiliations if affil.cgac is not None]
    assert len(cgac_affils) == 2
    abc_aff, def_aff = list(sorted(cgac_affils, key=lambda a: a.cgac.cgac_code))
    assert abc_aff.cgac.cgac_code == 'ABC'
    assert abc_aff.frec is None
    assert abc_aff.permission_type_id == PERMISSION_TYPE_DICT['submitter']
    assert def_aff.cgac.cgac_code == 'DEF'
    assert def_aff.frec is None
    assert def_aff.permission_type_id == PERMISSION_TYPE_DICT['reader']

    # one CGAC DABS from two strings, one CGAC FABS
    accountHandler.set_max_perms(user, 'prefix-CGAC_ABC-PERM_R,prefix-CGAC_ABC-PERM_S,prefix-CGAC_ABC-PERM_F')
    database.session.commit()   # populate ids
    assert len(user.affiliations) == 2
    affiliations = list(sorted(user.affiliations, key=lambda a: a.permission_type_id))
    dabs_aff, fabs_aff = affiliations
    assert dabs_aff.cgac.cgac_code == 'ABC'
    assert dabs_aff.frec is None
    assert dabs_aff.permission_type_id == PERMISSION_TYPE_DICT['submitter']
    assert fabs_aff.cgac.cgac_code == 'ABC'
    assert fabs_aff.frec is None
    assert fabs_aff.permission_type_id == PERMISSION_SHORT_DICT['f']

    # one FREC DABS from two strings, one FREC FABS, extra readonly CGAC for historical data
    accountHandler.set_max_perms(user, 
        'prefix-CGAC_ABC-FREC_ABC-PERM_R,prefix-CGAC_ABC-FREC_ABC-PERM_S,prefix-CGAC_ABC-FREC_ABC-PERM_F')
    database.session.commit()   # populate ids
    assert len(user.affiliations) == 3
    frec_affils = [affil for affil in user.affiliations if affil.frec is not None]
    assert len(frec_affils) == 2
    dabs_aff, fabs_aff = list(sorted(frec_affils, key=lambda a: a.permission_type_id))
    assert dabs_aff.cgac is None
    assert dabs_aff.frec.frec_code == 'ABC'
    assert dabs_aff.permission_type_id == PERMISSION_TYPE_DICT['submitter']
    assert fabs_aff.cgac is None
    assert fabs_aff.frec.frec_code == 'ABC'
    assert fabs_aff.permission_type_id == PERMISSION_SHORT_DICT['f']
    cgac_affils = [affil for affil in user.affiliations if affil.cgac is not None]
    assert len(cgac_affils) == 1
    assert cgac_affils[0].cgac.cgac_code == 'ABC'
    assert cgac_affils[0].frec is None
    assert cgac_affils[0].permission_type_id == PERMISSION_TYPE_DICT['reader']


@pytest.mark.usefixtures("user_constants")
def test_create_session_and_response(database, monkeypatch):
    cgacs = [CGACFactory(cgac_code=str(i) * 3, agency_name=str(i)) for i in range(3)]
    user = UserFactory(name="my name", title="my title", affiliations=[
        UserAffiliation(cgac=cgacs[1], permission_type_id=PERMISSION_TYPE_DICT['reader']),
        UserAffiliation(cgac=cgacs[2], permission_type_id=PERMISSION_TYPE_DICT['writer']),
    ])
    database.session.add_all(cgacs + [user])
    database.session.commit()
    monkeypatch.setattr(accountHandler, 'LoginSession', Mock())

    result = accountHandler.AccountHandler.create_session_and_response(Mock(), user)
    result = json.loads(result.data.decode('utf-8'))
    assert result['message'] == 'Login successful'
    assert result['user_id'] == user.user_id
    assert result['name'] == 'my name'
    assert result['title'] == 'my title'
    assert dict(agency_name='1', permission='reader') in result['affiliations']
    assert dict(agency_name='2', permission='writer') in result['affiliations']
