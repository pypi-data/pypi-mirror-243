# decision_lab

`pip install decisionlab`

## Introduction

`decision_lab` is a Python library that provides a simple and intuitive interface for creating and managing "decisions" that can be accessed via APIs. With `decision_lab`, you can make code behavior changes without changing the code itself, saving time and money on development and maintenance.

## Key Features

- Create and edit decisions through a user-friendly interface.
- Access decisions via APIs to make code behavior changes without modifying the codebase.
- Improve user experience and business outcomes with flexible and scalable decision management.

## Use Cases

- Change the welcome message on a website header by editing a decision in the UI, and the change will be reflected on the website.
- Modify the user list in a backend Python code by calling `decision.user_list`, without making changes to the codebase.

## Getting Started

DecisionLab Class
The DecisionLab class is a handy tool designed to interact with the Decision Lab API, allowing users to perform various tasks such as listing decisions, updating decision values, and retrieving specific decision values using provided tokens.

Initialization
To get started, you'll need to create an instance of the DecisionLab class in Python:

```
from decisionlab import DecisionLab
dlab = DecisionLab(token='your_token')
```
Here, token is a required parameter, and it should be your authentication token for API access. You can use either a read-only or a read-write token, depending on your needs.

Example Usage
Let's dive into some practical examples to see how you can use the DecisionLab class.

1. Listing Decisions with a Read-Only Token
If you want to list decisions with a read-only token, you can do so like this:

```
dlab = DecisionLab(token='your_read_only_token')
decisions = dlab.list_decisions()
print(decisions)
```
Expected Outcome:

This will return a list of decisions, such as` ['decision1', 'decision2',]`. Please note that this operation can only be performed with a read-only token.

2. Attempting to Update Decision Value with a Read-Only Token
If you attempt to update a decision value with a read-only token, you'll encounter a PermissionError. This is because updating a decision value requires a read-write token.

```
dlab.update_decision_value('decision_name', new_value)
```
Expected Outcome:

You'll receive an error message indicating that you do not have the necessary permissions to update the decision value.

3. Handling Invalid Token
In case you provide an invalid token, the DecisionLab class will handle it gracefully:

```
dlab = DecisionLab(token='invalid_token')
decisions = dlab.list_decisions()
print(decisions)
```
Expected Outcome:

You'll receive an error message, indicating that there are access issues or that the provided token is invalid.

4. Listing Decisions and Updating Values with a Read-Write Token
To both list decisions and update their values, you should use a read-write token and specify it as such when initializing the DecisionLab class:

```
dlab = DecisionLab(token='your_read_write_token', is_read_write=True)
decisions = dlab.list_decisions()
print(decisions)

dlab.update_decision_value('decision_name', new_value)
```
Expected Outcome:

This will list the decisions available for the given token and successfully update the value of the specified decision.
with a json `{'success': True}`
Methods
