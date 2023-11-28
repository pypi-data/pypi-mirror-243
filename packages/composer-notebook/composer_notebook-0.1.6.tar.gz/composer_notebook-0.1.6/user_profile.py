import os
from pydantic import BaseModel
from typing import List
import yaml

# Define the Pydantic models
class Holding(BaseModel):
    currency: str
    amount: float

class Portfolio(BaseModel):
    holdings: List[Holding]
    total_investment_value: float
    preferred_exchange: str
    wallet_history: dict

class InvestmentPreferences(BaseModel):
    preferred_cryptocurrencies: List[str]
    investment_strategy: str
    risk_tolerance: str
    time_horizon: str
    interests: List[str]
    history: List[str]

class UserProfile(BaseModel):
    personal_info: dict
    investment_preferences: InvestmentPreferences
    portfolio: Portfolio

    def format_profile(self):
        formatted_profile = f"Name: {self.personal_info['name']}\n"
        formatted_profile += f"Investment Strategy: {self.investment_preferences.investment_strategy} | "
        formatted_profile += f"Risk Tolerance: {self.investment_preferences.risk_tolerance} | "
        formatted_profile += f"Time Horizon: {self.investment_preferences.time_horizon}\n"
        formatted_profile += f"Interests: {', '.join(self.investment_preferences.interests)}\n"
        formatted_profile += f"History: {', '.join(self.investment_preferences.history)}\n"
        formatted_profile += f"Preferred Cryptocurrencies: {', '.join(self.investment_preferences.preferred_cryptocurrencies)}\n"
        formatted_profile += f"Portfolio Total Value: ${self.portfolio.total_investment_value}\n"
        formatted_profile += f"Holdings: {', '.join([f'{h.currency}: {h.amount}' for h in self.portfolio.holdings])}\n"
        formatted_profile += f"Preferred Exchange: {self.portfolio.preferred_exchange}\n"
        formatted_profile += f"Wallet Active Since: {self.portfolio.wallet_history['active_since']}"
        return formatted_profile

# Function to parse YAML data into a UserProfile object
def parse_user_profile(yaml_input):
    if isinstance(yaml_input, str) and os.path.exists(yaml_input) and yaml_input.endswith('.yaml'):
            with open(yaml_input, 'r') as file:
                yaml_data = yaml.safe_load(file)
            user_profile_data = yaml_data['UserProfile']
            return UserProfile(**user_profile_data)
    else:
        raise FileNotFoundError(f"No YAML file found at the given path: {yaml_input}")


