use thiserror::Error;

#[derive(Error, Debug)]
pub struct CompileError(pub String);

pub type CompileResult<A> = Result<A, CompileError>;

impl std::fmt::Display for CompileError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

#[derive(Error, Debug)]
pub enum VerificationError {
    #[error("encoding to encoded type failed: {0}")]
    Compile(#[from] CompileError),
    #[error("{0}")]
    Other(String),
}

impl From<String> for CompileError {
    fn from(error: String) -> Self {
        CompileError(error)
    }
}

impl From<String> for VerificationError {
    fn from(error: String) -> Self {
        VerificationError::Other(error)
    }
}

macro_rules! string_error {
    ($typeTo:ty, $typeFrom:ty) => {
        impl From<$typeFrom> for $typeTo {
            fn from(error: $typeFrom) -> Self {
                Self::from(error.to_string())
            }
        }
    };
}

string_error!(CompileError, &str);
string_error!(CompileError, base64::DecodeError);
string_error!(CompileError, prost::DecodeError);
string_error!(CompileError, serde_json::Error);
string_error!(CompileError, hex::FromHexError);
