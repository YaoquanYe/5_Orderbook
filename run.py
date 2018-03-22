from flask import *
from binance.client import Client
import pandas as pd
from Secret import *

app = Flask(__name__)

#Ask for secret code and get access to the Apikey and ApiSecret
secret_code = raw_input('Please enter the Secret code: ')
Apikey_decoded = web_auth_helper.decode(Apikey_encoded, secret_code)
ApiSecret_decoded = web_auth_helper.decode(ApiSecret_encoded, secret_code)

@app.route("/")
def show_tables():
        
        #Get the order book information from Binance
        client = Client(Apikey_decoded, ApiSecret_decoded)
        depth = client.get_order_book(symbol='ETHBTC')

        #Convert a dictionary to dataframe and remove the useless content
        df = pd.DataFrame.from_dict(depth)
        for index, row in df.iterrows():
            row['asks'].remove([])
            row['bids'].remove([])
        BidPart = df.drop('asks', axis=1)
        AskPart = df.drop('bids', axis=1)
        
        ##############################################################################

        #Split the original dataframe into two part.
        #Bid Part
        BidPrice = []
        BidSize = []
        
        for row in BidPart['bids']:
           BidPrice.append(row[0])
           BidSize.append(row[1])
           
        BidPart['BidPrice'] = BidPrice
        BidPart['BidSize'] = BidSize
        BidPart= BidPart.drop('bids', axis=1)
        BidPartDisplay = BidPart.drop('lastUpdateId',axis = 1)      
        
        #Ask Part       
        AskPrice = []
        AskSize = []
        
        for row in AskPart['asks']:
            AskPrice.append(row[0])
            AskSize.append(row[1])

        AskPart['AskPrice'] = AskPrice
        AskPart['AskSize'] = AskSize
        AskPart = AskPart.drop('asks', axis=1)
        AskPartDisplay = AskPart.drop('lastUpdateId',axis = 1)
        
        ###############################################################################
        
        #Balance Monitor        
        balanceBTC = client.get_asset_balance(asset='BTC')
        balanceETH = client.get_asset_balance(asset='ETH')
        balanceBTC = pd.DataFrame(balanceBTC, index=[0])
        balanceETH = pd.DataFrame(balanceETH, index=[1])
        frames = [balanceBTC, balanceETH]
        balancewhole = pd.concat(frames)
        
        ###############################################################################
        
        #Return all two tables to webpage
    
        return render_template('view.html',tables=[BidPartDisplay.to_html(classes='BidPart'),
                                                   AskPartDisplay.to_html(classes='AskPart'),
                                                   balancewhole.to_html(classes='balancewhole')],
        titles = ['na', 'BidPart', 'AskPart', 'Balance'])

if __name__ == "__main__":
    app.run(debug=True)

