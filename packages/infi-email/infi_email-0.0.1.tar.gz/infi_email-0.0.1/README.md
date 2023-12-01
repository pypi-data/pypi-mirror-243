# Email Package

## Introduction

infi_email is a package that send email.

## Installation

Install the package via pipenv:

    pipenv install infi_email

## Features

- send_email function can send email from one email to others.


## Usage Example

### send_email

    from infi_email import send_email

    # Replace all variables to the variables you need

    from_email: str = "from email here"
    email_password: str = "your email password"
    
    mails: list[str] = ["to email here"]
    subject: str = "your subject"
    message: str = "your message"
    
    send_email(from_email, email_password, mails, subject, message)
