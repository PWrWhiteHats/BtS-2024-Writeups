use crate::app::Message;
use iced::widget::{self, column, container, row, text, Column};
use iced::{Alignment, Length};

#[derive(Debug)]
pub struct LoginPageState {
    pub message: Option<String>,
    pub page_type: LoginPageType,
    pub username: String,
    pub password: String,
}

#[derive(Debug, Clone)]
pub enum LoginPageType {
    Login,
    Register,
}

impl Default for LoginPageState {
    fn default() -> Self {
        Self {
            username: String::new(),
            password: String::new(),
            message: None,
            page_type: LoginPageType::Login,
        }
    }
}

pub fn button_text(s: &str) -> widget::Button<'_, Message> {
    widget::button(s).padding(10)
}

impl LoginPageState {
    pub fn draw<'a>(&self) -> Column<'a, Message> {
        let username_input = widget::text_input("username", &self.username)
            .on_input(Message::InputUsernameChange)
            .padding(10)
            .size(30);
        let password_input = widget::text_input("password", &self.password)
            .on_input(Message::InputPasswordChange)
            .padding(10)
            .size(30)
            .secure(true);

        let (page_text, page_event) = match self.page_type {
            LoginPageType::Login => ("Sign in", Message::LoginPageTryLogin),
            LoginPageType::Register => ("Register", Message::LoginPageTryRegister),
        };
        let (switch_target, switch_event) = match self.page_type {
            LoginPageType::Login => (
                "Go to Register",
                Message::SetLoginPageType(LoginPageType::Register),
            ),
            LoginPageType::Register => (
                "Go to Login",
                Message::SetLoginPageType(LoginPageType::Login),
            ),
        };

        let button_row = container(
            row![
                button_text(page_text).on_press(page_event),
                button_text(switch_target).on_press(switch_event)
            ]
            .spacing(10),
        );

        // Override default text if there is a message
        let page_text = if let Some(text) = &self.message {
            text
        } else {
            page_text
        };

        column![text(page_text).size(50)]
            .spacing(20)
            .push(username_input)
            .push(password_input)
            .push(row![button_row].align_items(Alignment::End).spacing(10))
            .width(Length::Fill)
    }
}
pub fn draw_error<'a>(error: &str) -> Column<'a, Message> {
    column![
        text(error).size(50),
        button_text("Go back to login").on_press(Message::SetLoginPageType(LoginPageType::Login))
    ]
}
