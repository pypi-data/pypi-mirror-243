//! Error types

use std::{error::Error as StdError, fmt::Debug};

use thiserror::Error;

use crate::value::SerializationError;

pub type Result<T> = std::result::Result<T, Error>;

#[cfg(feature = "py")]
impl From<Error> for pyo3::PyErr {
    fn from(value: Error) -> pyo3::PyErr {
        // TODO select more accurate python error type
        pyo3::exceptions::PyException::new_err(value.to_string())
    }
}

impl From<Box<dyn StdError>> for Error {
    fn from(v: Box<dyn StdError>) -> Self {
        Error::Other(v.to_string())
    }
}

#[derive(Debug, Error)]
pub enum Error {
    #[error("Unsupported metadata: {0}")]
    UnsupportedMetadata(String),
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    #[cfg(feature = "json")]
    #[error("JSON error: {0}")]
    Json(#[from] serde_json::Error),
    #[cfg(feature = "neo4j")]
    #[error("Async error: {0}")]
    Neo4j(#[from] neo4rs::Error),
    #[cfg(feature = "neo4j")]
    #[error("Unsupported metadata format")]
    MetadataFormat,
    #[cfg(feature = "neo4j")]
    #[error("Invalid graph structure: {0}")]
    GraphStructure(String),
    #[error("Reading not supported by backend")]
    ReadUnsupported,
    #[error("Removing not supported by backend")]
    RemoveUnsupported,
    #[error("Serialization error: {0}")]
    Serialization(#[from] SerializationError),
    #[error("Invalid UUID: {0}")]
    IdError(#[from] uuid::Error),
    #[error("Could not parse hex string: {0}")]
    HexParser(#[from] hex::FromHexError),
    #[error("{0}")]
    Other(String),
}
