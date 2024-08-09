# from models.openai_model import get_openai_model
from models.azure_openai_model import get_azure_openai_model
from tools.incident_loader_tool import incident_info_loader_tool
from utils.langgraph import create_agent


paxMexChatLLM = get_azure_openai_model()

paxMexChatIncidentSummaryAgent = create_agent(
    paxMexChatLLM,
    [incident_info_loader_tool],
    """ You are an assistant that analyses customer incident data and generate a summary
                    When you are given incidentID to look at, use incident_info_loader_tool to get the incidentInfo
                    """,
)

paxMexChatIncidentResolutionAgent = create_agent(
    paxMexChatLLM,
    [incident_info_loader_tool],
    """ You are an assistant that analyses customer refund summary data, then provides a next best resolution. Rules:
                    Refund + Voucher: Provide refund if the order had a missing item and the value was high.
                    Immediate Refund: Provide immediate refund if the order had a missing item, and the value was average, and the customer complaint sentiment (extracted_text) is negative.
                    Self-Serve Refund: Provide refund if the item was missing and the value was average, and the customer complaint sentiment (extracted_text) is neutral.
                    Immediate Voucher: Provide an immediate voucher if the item is missing, the value is low, and the customer sentiment is negative (extracted_text).
                    If you find a special item in itemName or under the extracted_text column such as a cake or celebratory item for a party, then flag that as SPECIAL ITEM.
                    If you find an expensive item like waygu steak under the extracted_text column or itemName column, flat this as 'EXPENSIVE ITEM'""",
)

paxMexChatIncidentApologyAgent = create_agent(
    paxMexChatLLM,
    [incident_info_loader_tool],
    """ You are an assistant that generate an apology message to customer after the merchant already made the compensation.
                    You will be provided with rough summary of what the compensation have been done, and you need to generate an apology message to the customer.
                    *Example Input：
                    **generate apology message, I ve refund a full voucher to passenger
                    *Example Output
                    **Really sorry for your inconvenience, we have refunded a full voucher to you. We hope this will make up for the inconvenience you have experienced.
                    """,
)