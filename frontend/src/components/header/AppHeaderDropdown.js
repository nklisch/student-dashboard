import React from 'react'
import {
  CAvatar,
  CDropdown,
  CDropdownHeader,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import PropTypes from 'prop-types'

const AppHeaderDropdown = (props) => {
  return (
    <CDropdown variant="nav-item">
      <CDropdownToggle placement="bottom-end" className="py-0" caret={false}>
        <ProfileIcon {...props} />
      </CDropdownToggle>
      <CDropdownMenu className="pt-0" placement="bottom-end">
        <CDropdownHeader className="bg-light fw-semibold py-2 mb-1">Account</CDropdownHeader>
        <CDropdownItem href={'/'} onClick={props.logout}>
          <CIcon name="cil-user" className="me-2" />
          Profile
        </CDropdownItem>
        <CDropdownItem href={'/'} onClick={props.logout}>
          <CIcon name="cil-account-logout" className="me-2" />
          Logout
        </CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
  )
}

AppHeaderDropdown.propTypes = {
  logout: PropTypes.func.isRequired,
}

const ProfileIcon = (props) => {
  if (!props.user?.avatarUrl) {
    return (
      <CAvatar color="primary" size="md" textColor="white">
        <CIcon name="cil-user" />
      </CAvatar>
    )
  }

  return <CAvatar size="md" src={props.user.avatarUrl} />
}

ProfileIcon.propTypes = {
  user: PropTypes.object,
  avatarUrl: PropTypes.string,
}

export default AppHeaderDropdown
