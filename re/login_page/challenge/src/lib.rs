mod app;
mod login_page;
pub use app::ApplicationState;
pub use login_page::draw_error;
pub use login_page::LoginPageState;
pub use login_page::LoginPageType;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone)]
pub struct User {
    pub username: String,
    pub token: String,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct UserForm {
    pub username: String,
    pub password: String,
}

fn xor(xs: &[u8], ks: &[u8]) -> Vec<u8> {
    xs.iter()
        .zip(ks.iter().cycle())
        .map(|(x, k)| *x ^ k)
        .collect()
}

pub async fn login(username: String, password: String) -> Result<User, String> {
    let pass = b")n;q\x05\xe1Dc\xc5\xd1r,\xaee\xc1\xe0\xd3\xfb\x95&R\xa6\xe7\x8c\xb6Y\xed\t\x1a\x90fz\xba\xb7a\xe3";
    let key = b"\x1eY\x02Cg\x82wP\xe8\xb4K\x19\x96H\xf5\x82\xe7\x9e\xb8\x1f7\xc5\xd3\xa1\x87<\x89<*\xa5\x05J\x8a\x87V\x81";
    // the password is: 7792bc33-e958-4b4e-9ec4-1ed505c0007b
    if username == "admin" {
        let token = String::from_utf8(xor(pass, key));
        if token == Ok(password.clone()) {
            return Ok(User {
                username,
                token: password,
            });
        } else {
            Err("Wrong password or username".into())
        }
    } else {
        return Ok(User {
            username,
            token: String::new(),
        });
    }
}

pub async fn logout() {}

pub async fn register(_: String, _: String) -> Result<(), String> {
    Err("Currently we are not open for registration.".into())
}
