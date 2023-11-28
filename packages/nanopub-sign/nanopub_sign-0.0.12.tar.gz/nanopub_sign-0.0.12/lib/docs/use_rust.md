# 🦀 Use from Rust

[![crates.io](https://img.shields.io/crates/v/nanopub.svg)](https://crates.io/crates/nanopub)

You can use the Rust crate to easily sign, publish, or check a Nanopub:

```rust
use nanopub::{Nanopub, NpProfile};
use std::fs;
use tokio::runtime;

let public_key = r#"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAo2NYLBcZmpOkjgqLiT7hMxzRaK5KhYYHxxN2gCAMfmOaulAxAzPUNBJLIXjX3yQeIj6rAH4haWNAEUGPdiua/D+Pmu/Hrva3mK29lsWW9ajyZr0e12erDdaBw+3XfxMkKCZkLJjina6mi0W80e7Wa3+dsrypMDVl3CFYVvLsXu4lIMYqI2aVvbKyqCv6hUaWlGUip+2f84LQx/RSZGGwbBjwzKqe/Cs7frCW/lNlvsAkkst+IyFMcekEW875+rnsXP3phcP9Q1Ocu8wbnYYAu5lZPL19YFDSso2Qc5TpkXK3rawDYH36rOX8f0zBzdcbZAPx9btSCgXyqMpP8U4TCwIDAQAB"#;
let private_key = r#"MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCjY1gsFxmak6SOCouJPuEzHNForkqFhgfHE3aAIAx+Y5q6UDEDM9Q0EksheNffJB4iPqsAfiFpY0ARQY92K5r8P4+a78eu9reYrb2WxZb1qPJmvR7XZ6sN1oHD7dd/EyQoJmQsmOKdrqaLRbzR7tZrf52yvKkwNWXcIVhW8uxe7iUgxiojZpW9srKoK/qFRpaUZSKn7Z/zgtDH9FJkYbBsGPDMqp78Kzt+sJb+U2W+wCSSy34jIUxx6QRbzvn6uexc/emFw/1DU5y7zBudhgC7mVk8vX1gUNKyjZBzlOmRcretrANgffqs5fx/TMHN1xtkA/H1u1IKBfKoyk/xThMLAgMBAAECggEAECuG0GZA3HF8OaqFgMG+W+agOvH04h4Pqv4cHjYNxnxpFcNV9nEssTKWSOvCwYy7hrwZBGV3PQzbjFmmrxVFs20+8yCD7KbyKKQZPVC0zf84bj6NTNgvr6DpGtDxINxuGaMjCt7enqhoRyRRuZ0fj2gD3Wqae/Ds8cpDCefkyMg0TvauHSUj244vGq5nt93txUv1Sa+/8tWZ77Dm0s5a3wUYB2IeAMl5WrO2GMvgzwH+zT+4kvNWg5S0Ze4KE+dG3lSIYZjo99h14LcQS9eALC/VBcAJ6pRXaCTT/TULtcLNeOpoc9Fu25f0yTsDt6Ga5ApliYkb7rDhV+OFrw1sYQKBgQDCE9so+dPg7qbp0cV+lbb7rrV43m5s9Klq0riS7u8m71oTwhmvm6gSLfjzqb8GLrmflCK4lKPDSTdwyvd+2SSmOXySw94zr1Pvc7sHdmMRyA7mH3m+zSOOgyCTTKyhDRCNcRIkysoL+DecDhNo4Fumf71tsqDYogfxpAQhn0re8wKBgQDXhMmmT2oXiMnYHhi2k7CJe3HUqkZgmW4W44SWqKHp0V6sjcHm0N0RT5Hz1BFFUd5Y0ZB3JLcah19myD1kKYCj7xz6oVLb8O7LeAZNlb0FsrtD7NU+Hciywo8qESiA7UYDkU6+hsmxaI01DsttMIdG4lSBbEjA7t4IQC5lyr7xiQKBgQCN87YGJ40Y5ZXCSgOZDepz9hqX2KGOIfnUv2HvXsIfiUwqTXs6HbD18xg3KL4myIBOvywSM+4ABYp+foY+Cpcq2btLIeZhiWjsKIrw71+Q/vIe0YDb1PGf6DsoYhmWBpdHzR9HN+hGjvwlsYny2L9Qbfhgxxmsuf7zeFLpQLijjwKBgH7TD28k8IOk5VKec2CNjKd600OYaA3UfCpP/OhDl/RmVtYoHWDcrBrRvkvEEd2/DZ8qw165Zl7gJs3vK+FTYvYVcfIzGPWA1KU7nkntwewmf3i7V8lT8ZTwVRsmObWU60ySJ8qKuwoBQodki2VX12NpMN1wgWe3qUUlr6gLJU4xAoGAet6nD3QKwk6TTmcGVfSWOzvpaDEzGkXjCLaxLKh9GreM/OE+h5aN2gUoFeQapG5rUwI/7Qq0xiLbRXw+OmfAoV2XKv7iI8DjdIh0F06mlEAwQ/B0CpbqkuuxphIbchtdcz/5ra233r3BMNIqBl3VDDVoJlgHPg9msOTRy13lFqc="#;

let np_rdf = fs::read_to_string("./tests/resources/simple1-rsa.trig").unwrap();
let profile = NpProfile::new("https://orcid.org/0000-0000-0000-0000", "", &private_key, None).unwrap();

let signed_np = Nanopub::sign(&np_rdf, &profile).unwrap();
let checked_np = Nanopub::check(&signed_np.rdf).unwrap();

// Publish is async
let rt = runtime::Runtime::new().expect("Failed to create Tokio runtime");

let published_np = rt.block_on(async {
    Nanopub::publish(&np_rdf, &profile, None).await
}).unwrap();
println!("{}", published_np)
```

## 📖 API reference

Checkout the **[API documentation](https://docs.rs/nanopub)** for more details on how to use the different components and functions of the rust crate.
