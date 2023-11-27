#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SyntheticDataConf {
    #[prost(message, repeated, tag = "1")]
    pub columns: ::prost::alloc::vec::Vec<Column>,
    #[prost(bool, tag = "2")]
    pub output_original_data_stats: bool,
    #[prost(float, tag = "3")]
    pub epsilon: f32,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Mask {
    #[prost(enumeration = "mask::MaskFormat", tag = "1")]
    pub format: i32,
}
/// Nested message and enum types in `Mask`.
pub mod mask {
    #[derive(
        Clone,
        Copy,
        Debug,
        PartialEq,
        Eq,
        Hash,
        PartialOrd,
        Ord,
        ::prost::Enumeration
    )]
    #[repr(i32)]
    pub enum MaskFormat {
        GenericString = 0,
        GenericNumber = 1,
        Name = 2,
        Address = 3,
        Postcode = 4,
        PhoneNumber = 5,
        SocialSecurityNumber = 6,
        Email = 7,
        Date = 8,
        Timestamp = 9,
        Iban = 10,
    }
    impl MaskFormat {
        /// String value of the enum field names used in the ProtoBuf definition.
        ///
        /// The values are not transformed in any way and thus are considered stable
        /// (if the ProtoBuf definition does not change) and safe for programmatic use.
        pub fn as_str_name(&self) -> &'static str {
            match self {
                MaskFormat::GenericString => "GENERIC_STRING",
                MaskFormat::GenericNumber => "GENERIC_NUMBER",
                MaskFormat::Name => "NAME",
                MaskFormat::Address => "ADDRESS",
                MaskFormat::Postcode => "POSTCODE",
                MaskFormat::PhoneNumber => "PHONE_NUMBER",
                MaskFormat::SocialSecurityNumber => "SOCIAL_SECURITY_NUMBER",
                MaskFormat::Email => "EMAIL",
                MaskFormat::Date => "DATE",
                MaskFormat::Timestamp => "TIMESTAMP",
                MaskFormat::Iban => "IBAN",
            }
        }
        /// Creates an enum from field names used in the ProtoBuf definition.
        pub fn from_str_name(value: &str) -> ::core::option::Option<Self> {
            match value {
                "GENERIC_STRING" => Some(Self::GenericString),
                "GENERIC_NUMBER" => Some(Self::GenericNumber),
                "NAME" => Some(Self::Name),
                "ADDRESS" => Some(Self::Address),
                "POSTCODE" => Some(Self::Postcode),
                "PHONE_NUMBER" => Some(Self::PhoneNumber),
                "SOCIAL_SECURITY_NUMBER" => Some(Self::SocialSecurityNumber),
                "EMAIL" => Some(Self::Email),
                "DATE" => Some(Self::Date),
                "TIMESTAMP" => Some(Self::Timestamp),
                "IBAN" => Some(Self::Iban),
                _ => None,
            }
        }
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Column {
    #[prost(int32, tag = "1")]
    pub index: i32,
    #[prost(message, optional, tag = "2")]
    pub r#type: ::core::option::Option<::delta_sql_worker_api::ColumnType>,
    #[prost(message, optional, tag = "3")]
    pub mask: ::core::option::Option<Mask>,
}
