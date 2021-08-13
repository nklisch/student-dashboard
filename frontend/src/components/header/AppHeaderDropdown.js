import React from 'react'
import {
  CAvatar,
  CBadge,
  CDropdown,
  CDropdownDivider,
  CDropdownHeader,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { LOGIN_PATH } from 'src/globals'
import PropTypes from 'prop-types'
const AppHeaderDropdown = ({ isAuthenticated, user, logout }) => {
  let path = LOGIN_PATH
  let clickFunction = () => {}
  let action = 'Login'
  let icon = ''
  if (isAuthenticated) {
    path = '/'
    clickFunction = logout
    action = 'Logout'
    icon = 'cli-account-logout'
  }

  return (
    <CDropdown variant="nav-item">
      <CDropdownToggle placement="bottom-end" className="py-0" caret={false}>
        <CAvatar src="/avatars/8.jpg" size="md" />
      </CDropdownToggle>
      <CDropdownMenu className="pt-0" placement="bottom-end">
        <CDropdownHeader className="bg-light fw-semibold py-2">Settings</CDropdownHeader>
        <CDropdownItem href="#">
          <CIcon name="cli-user" className="me-2" />
          Profile
        </CDropdownItem>
        <CDropdownDivider />
        <CDropdownItem href={path} onClick={clickFunction}>
          <CIcon name={icon} className="me-2" />
          {action}
        </CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
  )
}

AppHeaderDropdown.propTypes = {
  isAuthenticated: PropTypes.bool.isRequired,
  user: PropTypes.object,
  logout: PropTypes.func.isRequired,
}

export default AppHeaderDropdown
