use iced::widget::{self, column, container, text};
use iced::{Application, Command, Length, Theme};

use crate::User;
use crate::{LoginPageState, LoginPageType};

#[derive(Debug)]
pub enum ApplicationState {
    Welcome,
    LoginPage { state: LoginPageState },
    ErrorGoBackToLogin { reason: String },
    LoggedIn { user: User },
}

#[derive(Debug, Clone)]
pub enum Message {
    Noop1,
    Noop2(()),
    InputUsernameChange(String),
    InputPasswordChange(String),
    SetLoginPageType(LoginPageType),
    LoginPageTryLogin,
    LoginPageTryRegister,
    LoginAttempt(Result<User, String>),
    RegisterAttempt(Result<(), String>),
    Logout,
}

impl Application for ApplicationState {
    type Executor = iced::executor::Default;
    type Message = Message;
    type Theme = Theme;
    type Flags = ();
    fn title(&self) -> String {
        match self {
            ApplicationState::Welcome => "Loading".into(),
            ApplicationState::LoginPage { .. } => "Login Page".into(),
            ApplicationState::ErrorGoBackToLogin { .. } => "Error".into(),
            ApplicationState::LoggedIn {
                user: User { username, .. },
            } => format!("Hello {username}!"),
        }
    }

    fn new(_flags: Self::Flags) -> (ApplicationState, iced::Command<Message>) {
        (
            ApplicationState::LoginPage {
                state: LoginPageState {
                    message: None,
                    page_type: LoginPageType::Login,
                    username: String::new(),
                    password: String::new(),
                },
            },
            Command::none(),
        )
    }

    fn update(&mut self, message: Message) -> iced::Command<Message> {
        match message {
            Message::Noop1 | Message::Noop2(_) => Command::none(),

            Message::InputUsernameChange(username_update) => {
                match self {
                    ApplicationState::LoginPage {
                        state:
                            LoginPageState {
                                ref mut username, ..
                            },
                    } => {
                        *username = username_update;
                    }
                    _ => unreachable!("InputUsernameChange called on non-login page"),
                };
                Command::none()
            }
            Message::InputPasswordChange(password_update) => {
                match self {
                    ApplicationState::LoginPage {
                        state:
                            LoginPageState {
                                username: _,
                                ref mut password,
                                ..
                            },
                    } => {
                        *password = password_update;
                    }
                    _ => unreachable!("InputPasswordChange called on non-login page"),
                };
                Command::none()
            }
            Message::SetLoginPageType(page_type) => {
                match self {
                    ApplicationState::LoginPage { ref mut state } => {
                        state.page_type = page_type;
                        state.message = None;
                    }
                    ApplicationState::ErrorGoBackToLogin { ref mut reason } => {
                        *self = ApplicationState::LoginPage {
                            state: LoginPageState {
                                message: Some(reason.to_owned()),
                                ..Default::default()
                            },
                        };
                    }
                    _ => unreachable!("SetLoginPageType Message from state: {:?}", self),
                };
                Command::none()
            }
            Message::LoginPageTryLogin => match self {
                ApplicationState::LoginPage {
                    state:
                        LoginPageState {
                            ref username,
                            ref password,
                            ..
                        },
                } => Command::perform(
                    super::login(username.to_owned(), password.to_owned()),
                    Message::LoginAttempt,
                ),
                _ => unreachable!(),
            },
            Message::LoginPageTryRegister => match self {
                ApplicationState::LoginPage {
                    state:
                        LoginPageState {
                            ref username,
                            ref password,
                            ..
                        },
                } => Command::perform(
                    super::register(username.to_owned(), password.to_owned()),
                    Message::RegisterAttempt,
                ),
                _ => unreachable!(),
            },
            Message::LoginAttempt(Ok(user)) => {
                *self = ApplicationState::LoggedIn { user };
                Command::none()
            }
            Message::RegisterAttempt(Ok(())) => {
                *self = ApplicationState::LoginPage {
                    state: LoginPageState {
                        message: Some("User registered. You may now login.".into()),
                        ..Default::default()
                    },
                };
                Command::none()
            }
            Message::RegisterAttempt(Err(str)) => {
                *self = ApplicationState::LoginPage {
                    state: LoginPageState {
                        message: Some(format!("Registration failed: {}", str)),
                        page_type: LoginPageType::Register,
                        ..Default::default()
                    },
                };
                Command::none()
            }
            Message::LoginAttempt(Err(error)) => {
                *self = ApplicationState::ErrorGoBackToLogin { reason: error };
                Command::none()
            }
            Message::Logout => {
                let username = match self {
                    ApplicationState::LoggedIn {
                        user: User { username, .. },
                    } => username,
                    _ => unreachable!(),
                };
                *self = ApplicationState::LoginPage {
                    state: LoginPageState {
                        message: Some(format!("User {} logged out. \nSign in", username)),
                        ..Default::default()
                    },
                };
                Command::perform(super::logout(), Message::Noop2)
            }
        }
    }
    fn view(&self) -> iced::Element<'_, Message, iced::Theme> {
        let flag = String::from(r"BtSCTF{Iced_Coffee_with_strings}");
        let content = match &self {
            ApplicationState::Welcome => {
                column![text("Hello World!").size(40),].width(Length::Shrink)
            }
            .width(Length::Shrink)
            .spacing(15),
            ApplicationState::LoginPage { state } => state.draw().max_width(520),
            ApplicationState::ErrorGoBackToLogin { reason } => crate::draw_error(reason),
            ApplicationState::LoggedIn { user } if user.username == "admin" => column![
                text(format!("Hello {}! the flag is: {flag}", user.username)).size(40),
                widget::button("Logout").on_press(Message::Logout)
            ],
            ApplicationState::LoggedIn { user } => column![
                text(format!("Hello {}!", user.username)).size(40),
                widget::button("Logout").on_press(Message::Logout)
            ]
            .width(Length::Shrink)
            .spacing(15),
        };

        container(content)
            .width(Length::Fill)
            .height(Length::Fill)
            .center_x()
            .center_y()
            .into()
    }
}
