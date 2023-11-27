mod proto;

use ::delta_attestation_api::AttestationSpecification;
pub use prost;
pub use proto::data_room::*;

impl From<ComputeNode> for configuration_element::Element {
    fn from(node: ComputeNode) -> Self {
        configuration_element::Element::ComputeNode(node)
    }
}

impl From<AttestationSpecification> for configuration_element::Element {
    fn from(attestation_spec: AttestationSpecification) -> Self {
        configuration_element::Element::AttestationSpecification(attestation_spec)
    }
}

impl From<UserPermission> for configuration_element::Element {
    fn from(user_permission: UserPermission) -> Self {
        configuration_element::Element::UserPermission(user_permission)
    }
}

impl From<AuthenticationMethod> for configuration_element::Element {
    fn from(authentication_method: AuthenticationMethod) -> Self {
        configuration_element::Element::AuthenticationMethod(authentication_method)
    }
}

impl configuration_element::Element {
    pub fn as_compute_node(&self) -> Option<&ComputeNode> {
        if let configuration_element::Element::ComputeNode(inner) = &self {
            Some(inner)
        } else {
            None
        }
    }

    pub fn as_attestation_specification(&self) -> Option<&AttestationSpecification> {
        if let configuration_element::Element::AttestationSpecification(inner) = &self {
            Some(inner)
        } else {
            None
        }
    }

    pub fn as_user_permission(&self) -> Option<&UserPermission> {
        if let configuration_element::Element::UserPermission(inner) = &self {
            Some(inner)
        } else {
            None
        }
    }

    pub fn as_authentication_method(&self) -> Option<&AuthenticationMethod> {
        if let configuration_element::Element::AuthenticationMethod(inner) = &self {
            Some(inner)
        } else {
            None
        }
    }
}

impl ConfigurationElement {
    pub fn as_compute_node(&self) -> Option<&ComputeNode> {
        self.element.as_ref()?.as_compute_node()
    }

    pub fn as_attestation_specification(&self) -> Option<&AttestationSpecification> {
        self.element.as_ref()?.as_attestation_specification()
    }

    pub fn as_user_permission(&self) -> Option<&UserPermission> {
        self.element.as_ref()?.as_user_permission()
    }

    pub fn as_authentication_method(&self) -> Option<&AuthenticationMethod> {
        self.element.as_ref()?.as_authentication_method()
    }
}
