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

const AppHeaderDropdown = ({ user, logout }) => {
  return (
    <CDropdown variant="nav-item">
      <CDropdownToggle placement="bottom-end" className="py-0" caret={false}>
        <ProfileIcon user={user} />
      </CDropdownToggle>
      <CDropdownMenu className="pt-0" placement="bottom-end">
        <CDropdownHeader className="bg-light fw-semibold py-2 mb-1">Account</CDropdownHeader>
        <CDropdownItem href={'/'}>
          <CIcon name="cil-user" className="me-2" />
          Profile
        </CDropdownItem>
        <CDropdownItem href={'/'} onClick={logout}>
          <CIcon name="cil-account-logout" className="me-2" />
          Logout
        </CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
  )
}

AppHeaderDropdown.propTypes = {
  logout: PropTypes.func.isRequired,
  user: PropTypes.object,
}

const ProfileIcon = ({ user }) => {
  const extractInitials = (fullname) => {
    let initials = ''
    for (const word of fullname.split(' ')) {
      initials += word[0]
    }
    return initials
  }
  return (
    <CAvatar src={user.avatar_url} color="primary" size="md" textColor="white">
      {`${extractInitials(user.name)}`}
    </CAvatar>
  )
}

ProfileIcon.propTypes = {
  user: PropTypes.object,
}

export default AppHeaderDropdown
