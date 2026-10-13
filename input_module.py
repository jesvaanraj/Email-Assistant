import streamlit as st


def get_email_details():

    st.subheader("Customer Email Input")

    col1, col2 = st.columns(2)

    with col1:

        customer_name = st.text_input(
            "Customer Name",
            placeholder="Enter customer name"
        )

    with col2:

        subject = st.text_input(
            "Email Subject",
            placeholder="Enter email subject"
        )

    customer_email = st.text_area(
        "Customer Email",
        placeholder="Enter the customer's message",
        height=150
    )

    return (
        customer_name,
        subject,
        customer_email
    )