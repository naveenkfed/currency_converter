import json
import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

'''
CURRENCIES = (
    'INR - Indian Rupees',
    'USD - US Dollars',
    'EUR - Euros',
    'GBP - British Pounds',
    'JPY - Japanese Yen',
    'DIR - Dirhams')
'''

def valid_input(value):
    if not value:
        raise ValueError('Amount cannot be empty.')
    
    if value.startswith('-'):
        raise ValueError('Amount cannot be negative.')
    
    try:
        float_val = float(value)
    
    except ValueError:
        raise ValueError('Invalid input for amount.')            
    
    return float_val


class SingleFrame(ttk.Frame):
    '''Class for Single Conversion Frame'''

    def __init__(self, master):
        """ Creates the GUI for the single converion Frame """
        super().__init__()
        self.master = master

        self.create_widgets()
        self.create_layout()
        self.add_trace()
    
    def create_widgets(self):
        """Creates the widgets"""
        self.lbl_amount = ttk.Label(
            master=self,
            text='Amount')     
            
        self.amount = tk.StringVar()
        self.ent_amount = ttk.Entry(
            master=self,
            textvariable=self.amount)
        
        self.lbl_from = ttk.Label(
            master=self,
            text='FROM')
         
        self.from_currency = tk.StringVar(value=CURRENCIES[0])
        self.from_combo = ttk.Combobox(
            master=self,
            textvariable=self.from_currency,
            width=30,
            values=CURRENCIES)
            
        self.lbl_to = ttk.Label(
            master=self,
            text='TO')
            
        self.to_currency = tk.StringVar(value=CURRENCIES[0])
        self.to_combo = ttk.Combobox(
            master=self,
            textvariable=self.to_currency,
            width=30,
            values=CURRENCIES)            
          
        self.output_var = tk.StringVar()
        self.lbl_output = ttk.Label(
            master=self,
            textvariable=self.output_var,
            font='Calibri 24 italic')

        self.btn_convert = ttk.Button(
            master=self,
            text='Convert',
            width=10,
            style='Convert.TButton',
            command=self.convert_value)

    def create_layout(self):
        """Creates the layout for the widgets"""
        self.lbl_amount.grid(
            row=1, column=0, padx=25, pady=25)
        
        self.ent_amount.grid(
            row=2, column=0)

        self.lbl_from.grid(
            row=1, column=1, padx=25, pady=25)
        
        self.from_combo.grid(
                row=2, column= 1, padx=75, pady=5)        

        self.lbl_to.grid(
            row=1, column=2, padx=25, pady=25)

        self.to_combo.grid(
            row=2, column= 2, padx=75, pady=5)

        self.lbl_output.grid(
            row=3, column = 0, columnspan=2, pady=100, sticky='w')

        self.btn_convert.grid(
            row=3, column=2, pady=100)
    
    def add_trace(self):
        """ Define callback handlers for tracing widget variables """
        self.amount.trace_add(
            mode='write',
            callback=lambda x, y, z: self.output_var.set(''))

        self.from_currency.trace_add(
            mode='write',
            callback=lambda x, y, z: self.output_var.set(''))

        self.to_currency.trace_add(
            mode='write',
            callback=lambda x, y, z: self.output_var.set(''))

    def convert_value(self):
        """ Callback for convert button  """
        try:
            float_val = valid_input(self.amount.get())
        
        except ValueError as err:
            self.output_var.set(err.args[0])
            return    
    
        fr_symbol = self.from_currency.get().split('-')[0].strip()
        to_symbol = self.to_currency.get().split('-')[0].strip() 
        exch_rate = EXCHANGE_RATES[fr_symbol][to_symbol]
        output_val = float_val * exch_rate

        self.output_var.set(
            f'{float_val} {fr_symbol} = {output_val} {to_symbol} \n\n'
            f'Exchange rate: \n 1 {fr_symbol} = {exch_rate} {to_symbol}')       


class BatchFrame(ttk.Frame):
    '''Class for Batch Conversion Frame'''

    def __init__(self, master):
        """Creates the GUI for the batch converion Frame """
        super().__init__()
        self.master = master

        self.create_widgets()
        self.create_layout()
        self.add_trace()        
    
    def create_widgets(self):
        """ Creates widgets """
        self.lbl_from = ttk.Label(
            master=self,
            text='FROM')

        self.from_currency = tk.StringVar(value=CURRENCIES[0])
        self.from_combo = ttk.Combobox(
            master=self,
            textvariable=self.from_currency,
            width=30,
            values=CURRENCIES)        
      
        self.lbl_to = ttk.Label(
            master=self,
            text='TO')
        
        self.to_currency = tk.StringVar(value=CURRENCIES[0])
        self.to_combo = ttk.Combobox(
            master=self,
            textvariable=self.to_currency,
            width=30,
            values=CURRENCIES)
     
        self.lbl_fpath = ttk.Label(
            master=self,
            text='Enter full path of the file.',
            font='Calibri 14')

        self.fpath = tk.StringVar()
        self.ent_fpath = ttk.Entry(
            master=self,
            width=95,
            textvariable=self.fpath)
        
        self.btn_open = ttk.Button(
            master=self,
            text='Open',
            command=lambda: self.fpath.set(f'{os.path.abspath(askopenfilename(initialdir=os.getcwd()))}'),
            width=5)

        self.btn_convert = ttk.Button(
            master=self,
            text='Convert',
            width = 10,
            style='Convert.TButton',
            command=self.convert_file)

        self.output_var = tk.StringVar()
        self.lbl_output = ttk.Label(
            master=self,
            textvariable=self.output_var,
            font='Calibri 20 italic')
   
    def create_layout(self):
        """ Creates the layout for the created widgets"""
        self.lbl_from.grid(
            row=0, column=0, padx=10, pady=10)

        self.from_combo.grid(
            row=1, column= 0, padx=10, pady=2)

        self.lbl_to.grid(
            row=0, column=1, padx=50, pady=10)

        self.to_combo.grid(
            row=1, column= 1, padx=50, pady=2)

        self.lbl_fpath.grid(
            row=2, column=0, pady=40, sticky='s')

        self.ent_fpath.grid(
            row=3, column=0, columnspan=2, sticky= 'w')

        self.btn_open.grid(
            row=3, column=2,sticky='sw')

        self.btn_convert.grid(
            row=4, column=2, pady=75)
        
        self.lbl_output.grid(
            row=4, column = 0, columnspan=2, pady=100, sticky='w')

    def add_trace(self):
        """ Define callback handlers for tracing widget variables """
        self.fpath.trace_add(
            mode='write',
            callback=lambda x, y, z: self.output_var.set(''))

        self.from_currency.trace_add(
            mode='write',
            callback=lambda x, y, z: self.output_var.set(''))

        self.to_currency.trace_add(
            mode='write',
            callback=lambda x, y, z: self.output_var.set(''))

    def convert_file(self):
        """ Callback for convert button  """
        fpath = self.fpath.get()
        if not os.path.isfile(fpath):
            self.output_var.set('Invalid file path')
            return
        
        self.output_var.set('Converting values in file')
        fname = os.path.splitext(os.path.basename(fpath))[0]
        
        with open(fpath, mode='r') as fp:
            values = fp.readlines()
        
        fr_symbol = self.from_currency.get().split('-')[0].strip()
        to_symbol = self.to_currency.get().split('-')[0].strip() 
        exch_rate = EXCHANGE_RATES[fr_symbol][to_symbol]

        output_values= []    
        for value in values:
            try:
                float_val = valid_input(value)

            except ValueError as err:
                self.output_var.set(f'File contains invalid input: \n{err.args[0]}')
                return
            
            output_values.append(float_val * exch_rate)
        
        output_fpath = os.path.join(
            os.path.dirname(fpath),
            f'{fname}_{fr_symbol}_{to_symbol}.txt')
        
        out_str = "\n".join(map(str, output_values))
        with open(output_fpath, mode='w') as wp:
            wp.write(out_str)
        
        self.output_var.set(f'Converted file placed in above directory. \n\n'
                f'Exchange rate: \n 1 {fr_symbol} = {exch_rate} {to_symbol}') 


def main():
    """ Entry point for the script"""
    window = tk.Tk()
    window.title('Currency Converter')

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Convert.TButton', font=('Calibri', 15, 'bold'), background='grey')
    style.configure('TLabel', font=('Calibri', 20, 'bold'))    

    tabs = ttk.Notebook(window)

    single_frame = SingleFrame(tabs)
    tabs.add(single_frame, text='Single Conversion')

    batch_frame = BatchFrame(tabs)
    tabs.add(batch_frame, text=' Batch Conversion')

    tabs.pack(expand=True, fill='both')
    window.mainloop()
        

if __name__ == '__main__':

    # Load exchange rates file
    with open('exchange_rates.json') as fp:
        EXCHANGE_RATES = json.load(fp)
  
    CURRENCIES = list(EXCHANGE_RATES.keys())
    main()