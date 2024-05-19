use login_page::ApplicationState;
use iced::{Application, Settings};

pub fn main() -> iced::Result {
    ApplicationState::run(Settings::default())
}
