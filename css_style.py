css_style = """
<style>
    body {
        margin: 0; /* Remove default margin */
        padding: 0; /* Remove default padding */
    }
    h1 {
        color: #1A1A1A; /* Change this to your desired color */
        font-size: 48px; /* Adjust the font size as needed */
        margin-top: 0; /* Remove top margin */
    }
    .stApp {
    background-color: #FFFFFF; /* Light gray background */
    }
    .stButton>button {
        background-color: #1f7ddc; /* Blue background */
        color: rgb(247, 241, 241); /* White text color */
    }
    .stMarkdown {
        color: #080808; /* Black Text Message Font */
        background-color: #EEF9F9; /* Light gray background color */
        padding: 5px; /* Padding around the text */
        border-radius: 5px; /* Rounded corners */
    }
    .stChatMessage {
        background-color: transparent !important; /* Makes the background transparent */
        border: none !important; /* Removes any borders */
        padding: 5px !important; /* Adjust this value to reduce padding */
    }
    .stBottomBlockContainer {
        background-color: #FFFFFF; /* White background color */
    }
    .custom-text-box {
        color: #080808; /* Black text color */
        background-color: #FFF9C0; /* Light yellow background color */
        padding: 5px; /* Padding around the text */
        border-radius: 10px; /* Rounded corners */
        margin-top: 1px; /* Space above the text box */
    }
</style>
"""

def get_css_style():
    return css_style