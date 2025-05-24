#!/usr/bin/env python
# coding: utf-8

# In[16]:

import tkinter as tk
from tkinter import messagebox
import bitget.v1.mix.order_api as maxOrderApi
import bitget.v1.mix.market_api as market_api
import bitget.v1.mix.account_api as account_api
import time
import bitget.bitget_api as bitget_api
from bitget.exceptions import BitgetAPIException
import tkinter as tk
from tkinter import ttk
import sys
import tkinter as tk
import threading
import time
import os


def show_error_message(error_msg):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Fehler", error_msg)


if __name__ == '__main__':
    # abo ahmed
    apiKey = "xxxx"
    secretKey = '''xxxx'''
    passphrase = "xxxx"

    try:
        maxOrderApi = maxOrderApi.OrderApi(apiKey, secretKey, passphrase)
        market_api = market_api.MarketApi(apiKey, secretKey, passphrase)
        account_api = account_api.AccountApi(apiKey, secretKey, passphrase)
        bitget_api = bitget_api.BitgetApi(apiKey, secretKey, passphrase)

        print("Verbunden")
    except BitgetAPIException as e:
        print("error: ", e)


# In[17]:


root = tk.Tk()


# In[18]:


# (USDT-M-Futures)            umcbl  = BTCUSDT_UMCBL       ETHUSDT_UMCBL       / quoteCoin = USDT     /supportMarginCoins = USDT
# (Coin-M Perptual-Futeres)   dmcbl  = BTCUSD_DMCBL        ETHUSD_DMCBL        /quoteCoin = USD       /supportMarginCoins = ['BTC', 'ETH', 'USDC', 'XRP', 'BGB', 'STETH']
# (USDC-M-Futures)            cmcbl  = BTCPERP_CMCBL       ETHPERP_CMCBL       /quoteCoin = USD       /supportMarginCoins = USDC
# (USDT-M-Futures Demo)       sumcbl = SBTCSUSDT_SUMCBL    SETHSUSDT_SUMCBL     /quoteCoin = SUSDT
# (Coin-M Futeres Demo)       sdmcbl = SBTCSUSD_SDMCBL     SETHSUSD_SDMCBL     /quoteCoin = SUSD
# (USDC-M-Futures Demo)       scmcbl = SBTCSPERP_SCMCBL    SETHSPERP_SCMCBL    /quoteCoin = SUSD

class Runden:

    def __init__(self):
        self.taziz_Max_Order = 0
        self.taziz_Unterschied = 0
        self.tazizArray = []  # 0 = startpreis
        self.first_Lot_taziz = 0
        self.Mal_Lot_taziz = 2
        self.LotArray_taziz = []
        self.TP = 0
        self.openPriceAvg = 0
        self.markPrice = 0
        self.Mal_Lot = 2
        self.data_position = None
        self.gradean = False
        self.weitere_runden = None
        self.Werte_in_sich = False
        self.TabridArray = []
        self.LotArray_tabrid = []
        self.available = 0
        # self.client_id = []  # die erste position ist keine order
        self.symbol = "BTCUSDT_UMCBL"
        self.productType = "umcbl"
        self.marginCoin = "USDT"
        self.symbolArray = []
        self.unrealizedPL = 0
        self.Unterschied = None
        self.TP_Prozent = 0
        self.Max_Order = None
        self.first_Lot = None
        self.Richtung = None
        self.start_Preis = 1000

    def reset_attributes(self):
        self.markPrice = 0
        self.openPriceAvg = 0
        self.TP = 0
        self.tazizArray = []
        self.data_position = None
        self.available = 0
        self.LotArray_tabrid = []
        # self.Werte_in_sich = False
        self.TabridArray = []
        self.client_id = []
        self.unrealizedPL = 0
        self.start_Preis = None
        
    def reset_Class(self):
        self.taziz_Max_Order = 0
        self.taziz_Unterschied = 0
        self.tazizArray = []  # 0 = startpreis
        self.first_Lot_taziz = 0
        self.Mal_Lot_taziz = 2
        self.LotArray_taziz = []
        self.TP = 0
        self.openPriceAvg = 0
        self.markPrice = 0
        self.Mal_Lot = 2
        self.data_position = None
        self.gradean = False
        self.weitere_runden = None
        self.Werte_in_sich = False
        self.TabridArray = []
        self.LotArray_tabrid = []
        self.available = 0
        # self.client_id = []  # die erste position ist keine order
        self.symbol = "BTCUSDT_UMCBL"
        self.productType = "umcbl"
        self.marginCoin = "USDT"
        self.symbolArray = []
        self.unrealizedPL = 0
        self.Unterschied = None
        self.TP_Prozent = 0
        self.Max_Order = None
        self.first_Lot = None
        self.Richtung = None
        self.start_Preis = 1000

    def berechne_TP(self):
        if self.Richtung == 'open_long':
            if self.TP_Prozent < 0:  # Überprüfung, ob TP_Prozent negativ ist
                self.TP_Prozent *= -1  # TP_Prozent wird positiv gemacht
            self.TP = self.openPriceAvg * (1 + self.TP_Prozent / 100)
        elif self.Richtung == 'open_short':
            if self.TP_Prozent > 0:  # Überprüfung, ob TP_Prozent positiv ist
                self.TP_Prozent *= -1  # TP_Prozent wird negativ gemacht
            self.TP = self.openPriceAvg * (1 + self.TP_Prozent / 100)

    def TP_Erreicht(self):
        if self.Richtung == 'open_long':
            return self.markPrice >= self.TP
        elif self.Richtung == 'open_short':
            return self.markPrice <= self.TP

    def print_attributes(self):
        attributes = vars(self)
        for attribute in attributes:
            print(attribute, ':', attributes[attribute])

    def AlleSymboleAnzeigen(self):
        params = {}
        params["productType"] = self.productType
        response = market_api.contracts(params)

        for item in response['data']:
            self.symbolArray.append(item['symbol'])

    def Rechnen_GV(self):
        self.data_position = None
        self.print_attributes()
        try:
            params = {}
            params["productType"] = self.productType
            params["symbol"] = self.symbol.split('_')[0]
            params["marginCoin"] = self.marginCoin

            try:
                response = bitget_api.get(
                    "/api/v2/mix/position/single-position", params)

            except BitgetAPIException as e:
                print("\n\n\n\n")
                print("except 1 ")
                self.print_attributes()
                print("e : ", e)
                print("params: ", params)
                print("\n\n\n\n")
                time.sleep(2)
                try:
                    response = bitget_api.get(
                        "/api/v2/mix/position/single-position", params)
                except BitgetAPIException as e:
                    print("\n\n\n\n")
                    print("except 2 ")
                    self.print_attributes()
                    print("e : ", e)
                    print("params: ", params)
                    print("\n\n\n\n")
                    time.sleep(2)
                    try:
                        response = bitget_api.get(
                            "/api/v2/mix/position/single-position", params)
                    except BitgetAPIException as e:
                        print("\n\n\n\n")
                        print("except 3 ")
                        self.print_attributes()
                        print("e : ", e)
                        print("params: ", params)
                        print("\n\n\n\n")
                        error_msg = "Bei Rechnen_GV()"
                        show_error_message(error_msg)

            data_Array = response['data']
            # Überprüft, ob das Array leer ist
            if not data_Array:
                print("Das position ist leer.")
            else:
                datap = data_Array[0]
                self.data_position = datap
                self.openPriceAvg = float(datap['openPriceAvg'])
                self.unrealizedPL = float(datap['unrealizedPL'])
                self.available = float(datap['available'])
                self.markPrice = float(datap['markPrice'])
                self.berechne_TP()
                if (self.TP_Erreicht() == True):
                    self.data_position = None
                    print("TP erreicht ")

        except BitgetAPIException as e:
            print("\n\n\n\n")
            self.print_attributes()
            print(e)
            print(params)
            print("\n\n\n\n")
            error_msg = "Bei Rechnen_GV()"
            show_error_message(error_msg)

    def close_all_positions(self):

        if (self.Richtung == "open_long"):
            side = "close_long"
        else:
            side = "close_short"
        try:
            params = {}
            params["symbol"] = self.symbol
            params["marginCoin"] = self.marginCoin
            params["side"] = side
            params["orderType"] = "market"
            params["size"] = self.available
            params["timInForceValue"] = "normal"
            response = maxOrderApi.placeOrder(params)

        except BitgetAPIException as e:
            print("close_all_positions(self) Keine Position Closed")
            # print(e)

    def get_market_price(self):
        params = {"symbol": self.symbol}
        data = market_api.ticker(params)
        market_price = data['data']['last']
        return market_price

    def lot_rechnen(self):
        self.LotArray_tabrid.append(round(self.first_Lot, 3))
        orderes = max(self.Max_Order, self.taziz_Max_Order) + 1
        while len(self.LotArray_tabrid) < orderes:
            prev_sum = sum(self.LotArray_tabrid)
            ergebnis = prev_sum * self.Mal_Lot
            self.LotArray_tabrid.append(round(ergebnis, 3))

        self.LotArray_taziz.append(round(0, 3))
        self.LotArray_taziz.append(round(self.first_Lot_taziz, 3))
        while len(self.LotArray_taziz) < orderes:
            prev_sum = sum(self.LotArray_taziz)
            ergebnis = prev_sum * self.Mal_Lot_taziz
            self.LotArray_taziz.append(round(ergebnis, 3))

    def Order_in_array(self):
        try:
            self.TabridArray.append(self.start_Preis)
            self.tazizArray.append(self.start_Preis)
            if self.Richtung == "open_long":
                for i in range(1, self.Max_Order + 1):
                    new_tabrid_value = self.TabridArray[i-1] - self.Unterschied
                    self.TabridArray.append(round(new_tabrid_value, 3))
                ##############################################################################
                for i in range(1, self.taziz_Max_Order + 1):
                    new_tabrid_value = self.tazizArray[i -
                                                       1] + self.taziz_Unterschied
                    self.tazizArray.append(round(new_tabrid_value, 3))
                ##############################################################################

            elif self.Richtung == "open_short":
                for i in range(1, self.Max_Order + 1):
                    new_tabrid_value = self.TabridArray[i-1] + self.Unterschied
                    self.TabridArray.append(round(new_tabrid_value, 3))
                ##############################################################################
                for i in range(1, self.taziz_Max_Order + 1):
                    new_tabrid_value = self.tazizArray[i -
                                                       1] - self.taziz_Unterschied
                    self.tazizArray.append(round(new_tabrid_value, 3))
                ##############################################################################

        except Exception as e:
            error_msg = "Order_in_array()"
            print(e)
            show_error_message(error_msg)

    def Order_Send_limit(self, preis, lot):
        try:
            params = {}
            params["symbol"] = self.symbol
            params["marginCoin"] = self.marginCoin
            params["side"] = self.Richtung
            params["orderType"] = "limit"
            params["price"] = preis
            params["size"] = lot
            params["timInForceValue"] = "normal"
            response = maxOrderApi.placeOrder(params)
            # response[0] = response
            # self.client_id.append(int(response[0]['data']['clientOid']))
        except Exception as e:
            # error_msg = "Order kann nicht gesendet werden (zu viel lot?)"
            print("Order kann nicht gesendet werden (zu viel lot?) : ")
            print(e)
            # show_error_message(error_msg)

    def Market_Order_Position(self):
        data = 0
        try:
            params = {}
            params["symbol"] = self.symbol
            params["marginCoin"] = self.marginCoin
            params["side"] = self.Richtung
            params["orderType"] = "market"
            params["size"] = self.first_Lot
            params["timInForceValue"] = "normal"
            response = maxOrderApi.placeOrder(params)

        except Exception as e:
            error_msg = "Roboter ist Aus Jetzt \nEs Könnte keine Market_Order_Position gemacht werden! \n(zu viel lot ?)"
            print(e)
            show_error_message(error_msg)
            root.destroy()
            os.system('exit')
            sys.exit()

        try:
            params = {}
            params["productType"] = self.productType
            params["symbol"] = self.symbol
            data = bitget_api.get(
                "/api/mix/v1/position/allPosition", params)
        except BitgetAPIException as e:
            error_msg = "Get Data Market_Order_Position()"
            print(e)
            show_error_message(error_msg)

        gesuchtes_symbol = self.symbol
        gesuchte_hold_side = 'long'  # oder 'short'
        if (self.Richtung == "open_long"):
            gesuchte_hold_side = 'long'
        elif (self.Richtung == "open_short"):
            gesuchte_hold_side = 'short'

        for item in data['data']:
            if item['symbol'] == gesuchtes_symbol and item['holdSide'] == gesuchte_hold_side:
                average_open_price_str = item['averageOpenPrice']
                average_open_price_float = float(
                    average_open_price_str)
                self.start_Preis = round(average_open_price_float, 6)
                self.openPriceAvg = self.start_Preis
                self.berechne_TP()
                break

    def Order_Send_to_Bitget(self):
        for k, elements in enumerate(self.TabridArray[1:], start=1):
            self.Order_Send_limit(
                preis=elements, lot=self.LotArray_tabrid[k])
######################################################################################################################

        for i, element in enumerate(self.tazizArray[1:], start=1):
            self.Order_Send_taziz(
                preis=element, lot=self.LotArray_taziz[i])

######################################################################################################################
    def Order_Loeschen(self):
        try:

            params = {}
            params["symbol"] = self.symbol
            params["marginCoin"] = self.marginCoin
            gg = bitget_api.post(
                "/api/mix/v1/order/cancel-symbol-orders", params)

        except BitgetAPIException as e:
            print("Order_Loeschen ()")
            print(e)
######################################################################################################################
        try:
            tparams = {}
            tparams["symbol"] = self.symbol
            tparams["planType"] = "normal_plan"
            trigerss = bitget_api.post(
                "/api/mix/v1/plan/cancelSymbolPlan", tparams)
        except BitgetAPIException as e:
            print("Trigger Order_Loeschen()")
            print(e)
######################################################################################################################

    def Order_Send_taziz(self, preis, lot):
        try:
            if (self.taziz_Unterschied > 0):
                params = {}
                params["symbol"] = self.symbol
                params["marginCoin"] = self.marginCoin
                params["size"] = lot
                params["triggerPrice"] = preis
                params["side"] = self.Richtung
                params["orderType"] = "market"
                params["triggerType"] = "fill_price"
                params["executePrice"] = preis
                response = bitget_api.post(
                    "/api/mix/v1/plan/placePlan", params)

        except BitgetAPIException as e:
            print("Order_Send_taziz() ")
            print(e)
######################################################################################################################

    def neue_Runde(self):
        try:
            self.gradean = True
            self.Market_Order_Position()
            self.lot_rechnen()
            self.Order_in_array()
            self.Order_Send_to_Bitget()
            print("die eingabe, die gesendet würden::")
            self.print_attributes()

        except Exception as e:
            print(e)
            error_msg = "neue_Runde()" + e
            show_error_message(error_msg)

    def Alles_schliessen(self):
        self.close_all_positions()
        self.Order_Loeschen()
        self.reset_attributes()


runde1 = Runden()
runde2 = Runden()
runde1.AlleSymboleAnzeigen()
runde2.AlleSymboleAnzeigen()


# In[19]:


class schleife:
    schleife_1 = True
    schleife_2 = True


# In[20]:


e = 18
L = 18


def flasch_Button():
    try:
        runde1.Alles_schliessen()
        runde2.Alles_schliessen()
        # runde1.reset_Class()
        # runde2.reset_Class()
        root.destroy()
        os.system('exit')
        sys.exit()

    except Exception as e:
        error_msg = str(e)
        show_error_message(error_msg)


def Ende2_Button():
    if (runde2.weitere_runden == True):
        runde2.weitere_runden = False
        ende2_button.config(bg="red")
        Rund1_label_Anzeigen()
        Rund2_label_Anzeigen()


def Ende1_Button():
    if (runde1.weitere_runden == True):
        runde1.weitere_runden = False
        ende1_button.config(bg="red")
        Rund1_label_Anzeigen()
        Rund2_label_Anzeigen()


def schleife_runde2():
    while schleife.schleife_2:
        try:
            runde2.Rechnen_GV()
        except Exception as e:
            time.sleep(2)
            try:
                runde2.Rechnen_GV()
            except Exception as e:
                time.sleep(2)
                try:
                    runde2.Rechnen_GV()
                except Exception as e:
                    print("Fehler: runde2.Rechnen_GV()")
                    runde2.print_attributes()
                    error_msg = "runde2.Rechnen_GV() " + str(e)
                    show_error_message(error_msg)
                    schleife.schleife_2 = False
                    break

        Rund1_label_Anzeigen()
        Rund2_label_Anzeigen()

        if not runde2.data_position:
            print("runde2: alles schließen")
            runde2.Alles_schliessen()
            if (runde2.weitere_runden == True):
                runde2.neue_Runde()
                print("runde2 neue_Runde")
                ende2_button.config(bg="white")
                Rund1_label_Anzeigen()
                Rund2_label_Anzeigen()

            elif (runde2.weitere_runden == False):
                runde2.reset_Class()
                print("runde2 reset_Class")
                ende2_button.config(bg="white")
                save_button.config(bg="green")
                Rund1_label_Anzeigen()
                Rund2_label_Anzeigen()
                if (runde1.weitere_runden == True and runde1.Werte_in_sich == True):
                    print("runde1 neue_Runde")
                    runde1.neue_Runde()
                    print("t1 wird gestartet")
                    t1 = None
                    schleife.schleife_1 = True
                    t1 = threading.Thread(target=schleife_runde1)
                    t1.start()
                else:
                    print("Exit")
                    root.destroy()
                    os.system('exit')
                    sys.exit()
                schleife.schleife_2 = False
        time.sleep(1)


def schleife_runde1():
    while schleife.schleife_1:

        try:
            runde1.Rechnen_GV()
        except Exception as e:
            time.sleep(2)
            try:
                runde1.Rechnen_GV()
            except Exception as e:
                time.sleep(2)
                try:
                    runde1.Rechnen_GV()
                except Exception as e:
                    print("Fehler: runde1.Rechnen_GV()")
                    runde1.print_attributes()
                    error_msg = "runde1.Rechnen_GV() " + str(e)
                    show_error_message(error_msg)
                    schleife.schleife_1 = False
                    break
        Rund1_label_Anzeigen()
        Rund2_label_Anzeigen()

        if not runde1.data_position:
            print("runde1: alles schließen")
            runde1.Alles_schliessen()
            if (runde1.weitere_runden == True):
                runde1.neue_Runde()
                print("runde1 neue_Runde")
                ende1_button.config(bg="white")
                # save_button.config(bg="green")
                Rund1_label_Anzeigen()
                Rund2_label_Anzeigen()

            elif (runde1.weitere_runden == False):
                runde1.reset_Class()
                print("runde1 reset_Class")
                ende1_button.config(bg="white")
                save_button.config(bg="green")
                Rund1_label_Anzeigen()
                Rund2_label_Anzeigen()
                if (runde2.weitere_runden == True and runde2.Werte_in_sich == True):
                    print("runde2 neue_Runde")
                    runde2.neue_Runde()
                    print("t2 wird gestartet")
                    t2 = None
                    schleife.schleife_2 = True
                    t2 = threading.Thread(target=schleife_runde2)
                    t2.start()
                else:
                    print("Exit")
                    root.destroy()
                    os.system('exit')
                    sys.exit()

                schleife.schleife_1 = False
        time.sleep(1)


def start_Button():
    if (runde1.Werte_in_sich == False):
        runde1.Werte_in_sich = True
        try:
            runde1.weitere_runden = True
            runde1.symbol = symbol_var.get()
            runde1.Unterschied = float(Tabrid_entry.get())
            runde1.first_Lot = float(Lot_entry.get())
            runde1.Mal_Lot = float(Mal_Lot_entry.get())
            runde1.Max_Order = int(Max_Order_entry.get())
            runde1.TP_Prozent = float(TP_Prozent_entry.get())
            ########################################################
            runde1.taziz_Max_Order = int(Max_Order_taziz_entry.get())
            runde1.taziz_Unterschied = float(taziz_entry.get())
            runde1.first_Lot_taziz = float(Lot_taziz_entry.get())
            runde1.Mal_Lot_taziz = float(Mal_Lot_taziz_entry.get())
            ########################################################
            Richtung = Richtung_var.get()

            if Richtung == "Buy":
                runde1.Richtung = "open_long"
            elif Richtung == "Sell":
                runde1.Richtung = "open_short"
            else:
                raise ValueError("Ungültige Richtung")

            try:
                Rund1_label_Anzeigen()
                Rund2_label_Anzeigen()

                if (runde1.Werte_in_sich == False or runde2.Werte_in_sich == False):
                    save_button.config(bg="green")
                elif (runde1.Werte_in_sich == True and runde2.Werte_in_sich == True):
                    save_button.config(bg="red")

                if (runde2.gradean == False):
                    runde1.neue_Runde()

                    t = threading.Thread(target=schleife_runde1)
                    t.start()

            except Exception as e:
                error_msg = str(e)
                show_error_message(error_msg)

        except Exception as e:
            runde1.reset_Class()
            error_msg = "Falsche Eingabe " + str(e)
            show_error_message(error_msg)
            # root.destroy()
            # sys.exit()

    elif (runde1.Werte_in_sich == True and runde2.Werte_in_sich == False):
        runde2.Werte_in_sich = True

        try:
            runde2.weitere_runden = True
            runde2.symbol = symbol_var.get()
            runde2.Unterschied = float(Tabrid_entry.get())
            runde2.first_Lot = float(Lot_entry.get())
            runde2.Mal_Lot = float(Mal_Lot_entry.get())
            runde2.Max_Order = int(Max_Order_entry.get())
            runde2.TP_Prozent = float(TP_Prozent_entry.get())
            ########################################################
            runde2.taziz_Max_Order = int(Max_Order_taziz_entry.get())
            runde2.taziz_Unterschied = float(taziz_entry.get())
            runde2.first_Lot_taziz = float(Lot_taziz_entry.get())
            runde2.Mal_Lot_taziz = float(Mal_Lot_taziz_entry.get())

            ########################################################
            Richtung = Richtung_var.get()
            if Richtung == "Buy":
                runde2.Richtung = "open_long"
            elif Richtung == "Sell":
                runde2.Richtung = "open_short"

        except Exception as e:
            runde2.reset_Class()
            error_msg = "Falsche Eingabe " + str(e)
            show_error_message(error_msg)
            # root.destroy()
            # sys.exit()

        if (runde1.Werte_in_sich == False or runde2.Werte_in_sich == False):
            save_button.config(bg="green")
        elif (runde1.Werte_in_sich == True and runde2.Werte_in_sich == True):
            save_button.config(bg="red")

        Rund1_label_Anzeigen()
        Rund2_label_Anzeigen()

    else:
        show_error_message("Keine Platz für Runde")
        # root.destroy()
        # sys.exit()


def Rund1_label_Anzeigen():
    Rund1_label.config(
        text=("Runde 1: \n" +
              "Grade An: " + str(runde1.gradean) + "\n" +
              "Nächte Runde: " + str(runde1.weitere_runden) + "\n" +
              "Werte_in_sich: " + str(runde1.Werte_in_sich) + "\n" +
              "Symbol: " + str(runde1.symbol) + "\n" +
              "UnrealizedPL: " + str(runde1.unrealizedPL) + "\n" +
              "TP Preis: " + str(runde1.TP) + "\n" +
              "TP_Prozent: " + str(runde1.TP_Prozent) + "\n" +
              "available: " + str(runde1.available) + "\n" +
              "Richtung: " + str(runde1.Richtung) + "\n" +
              "Tabrid: \n" +
              "Tabrid: " + str(runde1.Unterschied) + "\n" +
              "Lot: " + str(runde1.first_Lot) + "\n" +
              "Mal : " + str(runde1.Mal_Lot) + "\n" +
              "Max Order: " + str(runde1.Max_Order) + "\n" +
              "taziz: \n" +
              "taziz: " + str(runde1.taziz_Unterschied) + "\n" +
              "Lot: " + str(runde1.first_Lot_taziz) + "\n" +
              "Mal : " + str(runde1.Mal_Lot_taziz) + "\n" +
              "Max Order: " + str(runde1.taziz_Max_Order)
              ), justify="left"
    )


def Rund2_label_Anzeigen():
    Rund2_label.config(

        text=("Runde 2: \n" +
              "Grade An: " + str(runde2.gradean) + "\n" +
              "Nächte Runde: " + str(runde2.weitere_runden) + "\n" +
              "Werte_in_sich: " + str(runde2.Werte_in_sich) + "\n" +
              "Symbol: " + str(runde2.symbol) + "\n" +
              "UnrealizedPL: " + str(runde2.unrealizedPL) + "\n" +
              "TP Preis: " + str(runde2.TP) + "\n" +
              "TP_Prozent: " + str(runde2.TP_Prozent) + "\n" +
              "available: " + str(runde2.available) + "\n" +
              "Richtung: " + str(runde2.Richtung) + "\n" +
              "Tabrid: \n" +
              "Tabrid: " + str(runde2.Unterschied) + "\n" +
              "Lot: " + str(runde2.first_Lot) + "\n" +
              "Mal : " + str(runde2.Mal_Lot) + "\n" +
              "Max Order: " + str(runde2.Max_Order) + "\n" +
              "taziz: \n" +
              "taziz: " + str(runde2.taziz_Unterschied) + "\n" +
              "Lot: " + str(runde2.first_Lot_taziz) + "\n" +
              "Mal : " + str(runde2.Mal_Lot_taziz) + "\n" +
              "Max Order: " + str(runde2.taziz_Max_Order)
              ), justify="left"
    )


def Runde1_Entfernen():
    if (runde1.gradean == False):
        runde1.reset_Class()
        runde1.reset_attributes()
        save_button.config(bg="green")

        Rund1_label_Anzeigen()
        Rund2_label_Anzeigen()


def Runde2_Entfernen():
    if (runde2.gradean == False):
        runde2.reset_Class()
        runde2.reset_attributes()
        save_button.config(bg="green")
        Rund1_label_Anzeigen()
        Rund2_label_Anzeigen()


def on_closing():
    print("Das Fenster wird geschlossen")
    root.destroy()
    os.system('exit')
    sys.exit()


def GuiZeigen():

    global Tabrid_entry, Max_Order_entry, Mal_Lot_taziz_entry, Lot_taziz_entry, Max_Order_taziz_entry, taziz_entry, Runde2_Entfernen_button, Runde1_Entfernen_button, Lot_entry, Max_Order_entry, TP_Prozent_entry, Richtung_var, Mal_Lot_entry, save_button, ende1_button, ende2_button, flasch_button, symbol_var, Rund1_label, Rund2_label
    window_width = 1000
    window_height = 900

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    leer_label = tk.Label(
        root, text="                                   ", font=("Helvetica", L))
    leer_label.grid(row=0, column=0, sticky="w")

    leer_label = tk.Label(
        root, text="                                   ", font=("Helvetica", L))
    leer_label.grid(row=0, column=1, sticky="w")

    symbol_label = tk.Label(root, text="Symbol:", font=("Helvetica", L))
    symbol_label.grid(row=1, column=0, sticky="w")
    symbol_var = tk.StringVar()
    symbol_combobox = ttk.Combobox(
        root, textvariable=symbol_var, font=("Helvetica", e), width=14)
    symbol_combobox['values'] = runde1.symbolArray
    symbol_combobox.grid(row=1, column=1, sticky="ew")
    symbol_combobox.insert(0, runde1.symbol)

    Tabrid_label = tk.Label(
        root, text="Tabrid / Taziz:", font=("Helvetica", L))
    Tabrid_label.grid(row=2, column=0, sticky="w")
    Tabrid_entry = tk.Entry(root, font=("Helvetica", e), width=15)
    Tabrid_entry.grid(row=2, column=1, sticky="ew")
    Tabrid_entry.insert(0, "20")

    taziz_entry = tk.Entry(root, font=("Helvetica", e), width=15)
    taziz_entry.grid(row=2, column=2, sticky="ew")
    taziz_entry.insert(0, "20")

    Lot_label = tk.Label(root, text="First Lot:", font=("Helvetica", L))
    Lot_label.grid(row=3, column=0, sticky="w")
    Lot_entry = tk.Entry(root, font=("Helvetica", e), width=15)
    Lot_entry.grid(row=3, column=1, sticky="ew")
    Lot_entry.insert(0, "0.1")

    Lot_taziz_entry = tk.Entry(root, font=("Helvetica", e), width=15)
    Lot_taziz_entry.grid(row=3, column=2, sticky="ew")
    Lot_taziz_entry.insert(0, "0.1")

    Mal_Lot_label = tk.Label(root, text="Mal ?:", font=("Helvetica", L))
    Mal_Lot_label.grid(row=4, column=0, sticky="w")
    Mal_Lot_entry = tk.Entry(root, font=("Helvetica", e), width=15)
    Mal_Lot_entry.grid(row=4, column=1, sticky="ew")
    Mal_Lot_entry.insert(0, "2")

    Mal_Lot_taziz_entry = tk.Entry(root, font=("Helvetica", e), width=15)
    Mal_Lot_taziz_entry.grid(row=4, column=2, sticky="ew")
    Mal_Lot_taziz_entry.insert(0, "2")

    Max_Order_label = tk.Label(root, text="Max Order:", font=("Helvetica", L))
    Max_Order_label.grid(row=5, column=0, sticky="w")
    Max_Order_entry = tk.Entry(root, font=("Helvetica", e), width=15)
    Max_Order_entry.grid(row=5, column=1, sticky="ew")
    Max_Order_entry.insert(0, "4")

    Max_Order_taziz_entry = tk.Entry(root, font=("Helvetica", e), width=15)
    Max_Order_taziz_entry.grid(row=5, column=2, sticky="ew")
    Max_Order_taziz_entry.insert(0, "2")

    TP_Prozent_label = tk.Label(
        root, text="TP_Prozent:", font=("Helvetica", L))
    TP_Prozent_label.grid(row=6, column=0, sticky="w")
    TP_Prozent_entry = tk.Entry(root, font=("Helvetica", e), width=15)
    TP_Prozent_entry.grid(row=6, column=1, sticky="ew")
    TP_Prozent_entry.insert(0, "10")

    Richtung_label = tk.Label(root, text="Richtung:", font=("Helvetica", L))
    Richtung_label.grid(row=7, column=0, sticky="w")
    Richtung_var = tk.StringVar()
    Richtung_combobox = ttk.Combobox(
        root, textvariable=Richtung_var, font=("Helvetica", e), width=14)
    Richtung_combobox['values'] = ('Buy', 'Sell')
    Richtung_combobox.grid(row=7, column=1, sticky="ew")

    save_button = tk.Button(root, text="      حفظ      ", font=(
        "Helvetica", L), command=start_Button)
    save_button.grid(row=8, column=0)
    save_button.config(bg="green")

    ende1_button = tk.Button(root, text="    1 ايقاف تداول    ", font=(
        "Helvetica", L), command=Ende1_Button)
    ende1_button.grid(row=8, column=1, pady=5)
    ende1_button.config(bg="white")

    ende2_button = tk.Button(root, text="    2 ايقاف تداول    ", font=(
        "Helvetica", L), command=Ende2_Button)
    ende2_button.grid(row=9, column=1, pady=5)
    ende2_button.config(bg="white")

    flasch_button = tk.Button(root, text=" SOFOT Alles AUS ", font=(
        "Helvetica", L), command=flasch_Button)
    flasch_button.grid(row=8, column=2)
    flasch_button.config(bg="red")

    Rund1_label = tk.Label(root, text="Runde 1:", font=("Helvetica", L))
    Rund1_label.grid(row=9, column=0, sticky="w")

    Rund2_label = tk.Label(root, text="Runde 2:", font=("Helvetica", L))
    Rund2_label.grid(row=9, column=2, sticky="w")

    Runde1_Entfernen_button = tk.Button(root, text="      مسح      ", font=(
        "Helvetica", L), command=Runde1_Entfernen)
    Runde1_Entfernen_button.grid(row=10, column=0)
    Runde1_Entfernen_button.config(bg="white")

    Runde2_Entfernen_button = tk.Button(root, text="      مسح      ", font=(
        "Helvetica", L), command=Runde2_Entfernen)
    Runde2_Entfernen_button.grid(row=10, column=2)
    Runde2_Entfernen_button.config(bg="white")

    root.protocol("WM_DELETE_WINDOW", on_closing)

    Rund1_label_Anzeigen()
    Rund2_label_Anzeigen()
    root.title("Robot 1")
    root.mainloop()


GuiZeigen()
