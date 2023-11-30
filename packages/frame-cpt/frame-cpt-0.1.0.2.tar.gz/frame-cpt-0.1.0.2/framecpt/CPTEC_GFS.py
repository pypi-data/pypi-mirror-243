from datetime  import datetime, timedelta
import numpy as np
import pandas as pd
import json
import gc
import pycurl
import io
import xarray as xr
import time, random, glob, shutil, os, re
import warnings
warnings.filterwarnings('ignore')

class model(object):

    def __init__(self):

        """ 
            Função para inicializar o configurador do modelo GFS, retorna objeto com a função load habilitada para uso.

            Parametros
            ------------------------------------------------------------------------------------------------------------------------------------------------------       

            * Model     : Para configurar o GFS em novas resoluções altere o campo parameter
            * Variables : Para habilitar novas váriaveis adicionar o nome da variavel e o nome referente dentro do .idx ou .inv
            * Levels    : Define as variaveis com 1 unico nivel ou multiplos
            * Area      : Durante inicialização é adicionado o campo Reduce, quando True os parametros definidos aqui são aplicados para dar zoom em area desejada
            * Transform : Realiza transformação nas unidades das variaveis para uma unidade comum entre os modelos.
            * File      : Nome do arquivo disponivel no ftp
            * Server    : Servidor FTP consumido pela aplicação
            ------------------------------------------------------------------------------------------------------------------------------------------------------       

            Retorna objeto model
        """

        self.dict = {   
            
            "model"    : {
                    "name" : "GFS",
                    "parameter" : "0p25",
                    "long_name" : " National Centers for Environmental Prediction - NCEP "
            },
            "variables" :  {
                    "t" : "TMP",
                    "u" : "UGRD",
                    "v" : "VGRD",
                    "rh" : "RH",
                    "g" : "HGT",
                    "omega" : "VVEL",
                    "u10m" : "UGRD",
                    "v10m" : "VGRD",
                    "t2m" : "TMP",
                    "slp" : "PRMSL",
                    "psfc" : "PRES",
                    "terrain" : "HGT",
                    "sbcape" : "CAPE",
                    "sbcin" : "CIN",
                    "pw" : "PWAT",
                    "precip" : "APCP"
                        },
            "levels" :   {  
                        "t" : "LVL",
                        "u" : "LVL",
                        "v" : "LVL",
                        "rh" : "LVL",
                        "g" : "LVL",
                        "omega" : "LVL",
                        "u10m" : "SFC",
                        "v10m" : "SFC",
                        "t2m" : "SFC",
                        "slp" : "SFC",
                        "psfc" : "SFC",
                        "terrain" : "SFC",
                        "sbcape" : "SFC",
                        "sbcin" : "SFC",
                        "pw" : "SFC",
                        "precip" : "SFC"
            },
            "area"    : {
                        "minlat" :    -57,
                        "maxlat" :     17,
                        "minlon" :    277,
                        "maxlon" :    332
            },
            "transform" : {
                        "t"      : "-273.15",
                        "omega"  :     "*10",
                        "t2m"    :  "-273.15",
                        "slp"    :     "/100",
                        "psfc"   :     "/100"
            },
            "file"    : {
                        "name"   :     "gfs.t{}z.pgrb2.0p25.{}",
                        "format" :     "grib2"
            },
            "server":   {
                            "ftp"    :     "https://ftp.ncep.noaa.gov"
            }
    
        } 

        self.levels= [ "1000","975","950","925","900","850","800","750","700","650","600","550","500","450","400","350","300","250","200","150","100","70","50","40","30","20","15","10","7","5","3","2","1"]
       
        self.area = {
                       "northlat" :    90,
                       "southlat" :    -90,
                       "westlon" :    0,
                       "eastlon" :    360,
                       "invertedlat" : False
        }
        
        self.dict['area'].update({'reduce': False})
        self.dict.update({'save_netcdf': False})
        self.dict.update({'path_to_save': os.getcwd()})

        self.local_path = f"INPE/{self.dict['model']['name']}/{self.dict['model']['parameter']}/brutos"
        self.ftppath = f"/data/nccf/com/gfs/prod"

        print(f"\n#### {self.dict['model']['long_name']} ({self.dict['model']['parameter']}) #####\n")
        start = time.strftime("%Y%m%d", time.gmtime(time.time()))
        end = (datetime.strptime(f'{start}',  '%Y%m%d') - timedelta(days=9)).strftime("%Y%m%d")
        
        self.daterange =  pd.date_range(end, start)
        self.frequency = [0,168]        
        
        print(f"Forecast data available for reading between {end} and {start}.\n")
        print(f"Surface variables: t2m, u10m, v10m, slp, psfc, precip")
        print(f"                   terrain, sbcape, sbcin, pw.")
        print(f"Level variables:   t, u, v, rh, g, omega.\n")
        print(f"levels (hPa): 1000 975 950 925 900 850 800 750 700 650 600 550 500 450")
        print(f"              400 350 300 250 200 150 100 70 50 40 30 20 15 10 7 5 3 2 1.\n")
        print(f"Frequency: hourly frequency [0,1,2,...,22,23].\n")

        self.session = random.random()

        model.__clean__()

    def load(self, date=None, steps=[0], var=['t2m'], level=[1000, 'surface']):


        """
        
        A função load prepara a lista de variaveis, niveis e datas que serão carregadas para memoria.

        Durante execução um diretorio temporario é criado para manipular os arquivos e é apagado assim que finalizada requisição.

        self.date é definido pela frequência que o modelo disponibiliza suas previsões, para o GFS de 1 em 1 hora.

        Parametros
        ------------------------------------------------------------------------------------------------------------       
        date  : Data da condição inicial date=YYYYMMDDHH, use HH para IC 00 e 12.
        steps : Integer/Array de inteiros com os passos desejados. onde 0 é a inicialização do modelo [0,1, ... ,168], valor maximo 168.
        var   : Array de string com nome das variaveis disponiveis para leitura ['t2m', 'precip']
        level : Array de inteiros com os niveis disponiveis para cada modelo [1000, 850]
        ------------------------------------------------------------------------------------------------------------       

        load(date='2022082300', steps=[0,1,5,9], var=['t', 'precip'], level=[1000, 850])
        load(date='2022082300', steps= 4, var=['t', 'precip'], level=[1000, 850])
        
        ------------------------------------------------------------------------------------------------------------       
        
        Retorna um Xarray contendo todas variaveis solicitadas com as transformações contidas em self.dict

        ------------------------------------------------------------------------------------------------------------       

        """
        if (isinstance(steps,int)) : steps = [h for h in range(0, steps+1, 1)]
        if type(date) == int: date = str(date)
        if date == None: date = datetime.today().strftime("%Y%m%d")
        if type(level) == int: level = [level]
        if type(var) == str: var = [var]

        self.start_date = date
        self.start_date = self.start_date.replace('/', '')
        self.start_date = self.start_date.replace('-', '')
        if len(self.start_date) == 8: self.start_date = f"{self.start_date}00"

        self.query_level = level
        self.date = [(datetime.strptime(f'{self.start_date}',  '%Y%m%d%H') + timedelta(hours=int(h))).strftime("%Y%m%d%H") for h in steps]
        self.year       = self.start_date[0:4]
        self.mon        = self.start_date[4:6]
        self.day        = self.start_date[6:8]
        self.hour       = self.start_date[8:10]

        self.variables = var

        self.__getrange__()
        if os.path.exists(f".temporary_files/{self.session}"): shutil.rmtree(f".temporary_files/{self.session}")
        
        return self.file

    def __repr__(self):

        """
            Função para exibir definições contidas no objeto, acessivel através do self.dict

        """

        print(f"Reduce area: {self.dict['area']['reduce']}")
        print(f"Save netcdf: {self.dict['save_netcdf']}")
        print(f"Path to save: {self.dict['path_to_save']}")
        print(f"To see more info use wrf.help()")

        return str('')    

    def __clean__():

        """
            Quando o processo de requisição é interrompido a ferramenta não removerá os arquivos temporarios,
            esta função remove todo diretorio temporario com mais de 2 dias em disco.

        """

        if os.path.exists(f".temporary_files"): 

            today = datetime.today()
            
            files = glob.glob(".temporary_files/0.*")
            for f in files:
                duration = today - datetime.fromtimestamp(os.path.getmtime(f))
                if duration.days >= 2:
                    shutil.rmtree(f)
    
    def help(self):
        
        """
            Função para exibir as informações dos modelos e suas parametrizações.
        
        """
        print('help')

    def __getrange__(self):

        """ 
            Função para criar dataframe com informações que serão consumidas por self.__curl__.
            Entre as informações coletadas estão as posições inferior e superior de cada variavel dentro no arquivo grib.

            Exemplo self.setup:
            --------------------------------------------------------------------------------------------------------------       
                forecast_date      upper   id      lower  start_date  var    level   step_model varname fsim
            0   2022082300  405687910  563  405131549  2022082300  TMP  surface          anl     t2m  000
            1   2022082301  405723677  563  405166292  2022082300  TMP  surface  1 hour fcst     t2m  001
            --------------------------------------------------------------------------------------------------------------       

        """

        arr = []

        try:

            for id,dt in enumerate(self.date):
            
                fsim = f'{id}'
                fsim = fsim.zfill(3)

                invfile = self.dict['file']['name'].format(self.hour, f'f{fsim}')
                invfile = f'{self.ftppath}/gfs.{self.year}{self.mon}{self.day}/{self.hour}/atmos/{invfile}.idx'

                #print(f"{self.dict['server']['ftp']}/{invfile}")
                
                df = pd.read_csv(f"{self.dict['server']['ftp']}/{invfile}", skiprows=0, names=['header'])
                
                df['header'] = df['header'].map(lambda x: x[:-1])
                df[['id', 'allocate', 'date', 'var', 'level', 'timeFct']] = df['header'].str.split(':', expand=True)
                df.drop('header', axis=1, inplace=True)
                df['date'] = df['date'].map(lambda x: str(x).split('=')[1])
                
                for var in self.variables:
                    if var in self.dict['variables']:

                        value = self.dict['variables'][var]
                        varframe = df[ df['var'] == value ]

                        # Add 1000 and surface when not defined on request
                        tmp_list = [i for i in self.query_level if i != 'surface']
                        if self.dict['levels'][var] == 'LVL' and len(tmp_list) == 0:
                            self.query_level.append(1000)

                        tmp_list = [i for i in self.query_level if i == 'surface']
                        if self.dict['levels'][var] == 'SFC' and len(tmp_list) == 0:
                            self.query_level.append('surface')

                        for lvl in self.query_level:

                            if self.dict['levels'][var] == 'LVL' and lvl == 'surface':
                                pass
                            elif self.dict['levels'][var] == 'SFC' and lvl != 'surface':
                                pass
                            else:

                                if lvl == 'surface': 

                                    if var == 't2m' or value == 'TMP': lvl = '2 m above ground'
                                    
                                    if var == 'slp' or value == 'MSLET': lvl = 'mean sea level'

                                    if var == 'v10m' or var == 'u10m': lvl = '10 m above ground'

                                    if var == 'pw': lvl = 'considered as a single layer'

                                    if var == 'precip' and id == 0: pass

                                if len(varframe) == 1:

                                    frame = varframe

                                else:

                                    if self.dict['levels'][var] == 'SFC':

                                        if var == 'precip':

                                            frame = varframe[ varframe['timeFct'] == f'0-{id} hour acc fcst' ][-1:]
                                        else:
                                            frame = varframe[ varframe['level'] == lvl ]
                                    else:
                                        frame = varframe[ varframe['level'] == f'{lvl} mb' ]

                                if len(frame) > 0:

                                    upper = df.iloc[frame.index+1]['allocate']
                                    pp = np.append(dt, upper)
                                    
                                    try:
                                        pp = np.append(pp, frame.values[0])
                                    except IndexError:
                                        pp = np.append(pp, frame.values)
                                    
                                    pp = np.append(pp, var)
                                    pp = np.append(pp, fsim)

                                    arr.append(pp)
                                
            self.setup = pd.DataFrame(arr, columns=['forecast_date', 'upper', 'id',
                                                        'lower', 'start_date', 'var', 
                                                        'level', 'step_model', 'varname', 'fsim'])

            self.setup.drop_duplicates(inplace=True)
            self.__curl__()

        except:
            print('File not available on server!')
            self.file = None


    def __curl__(self):


        """
        
            A função __curl__ realiza para cada registro em self.setup o download das variaveis descritas, aplica as transformações
            definidas em self.dict['transform'] e devolve em self.file um Xarray em memoria com todos tempos das variaveis previstas solicitas.

            Quando self.dict['save_netcdf'] == True um arquivo netcdf4 será salvo com copia da requisição automaticamente.
        
        """

        pathout = f".temporary_files/{self.session}"

        os.makedirs(pathout, exist_ok=True)

        fidx = glob.glob(f"{pathout}/*.idx")
        if len(fidx) > 0:
            [os.remove(f) for f in fidx]
        
        for _,row in self.setup.iterrows():
            
            grbfile = self.dict['file']['name'].format(self.hour, f"f{row['fsim']}")
            grbfile = f'{self.ftppath}/gfs.{self.year}{self.mon}{self.day}/{self.hour}/atmos/{grbfile}'
            c = pycurl.Curl()
            c.setopt(pycurl.URL,f"{self.dict['server']['ftp']}/{grbfile}")

            outfile = self.dict['file']['name'].format(self.hour, row['fsim'])
            lvl = row['level'].replace(" ", "")
            outfile = f"{pathout}/{row['varname']}_{lvl}_{outfile}"

            with open(outfile, "wb") as fout:
                c.setopt(pycurl.WRITEDATA, fout)
                c.setopt(c.RANGE, f"{row['lower']}-{row['upper']}") 
                c.setopt(pycurl.VERBOSE, 0)
                c.setopt(pycurl.FOLLOWLOCATION, 0)
                c.perform()
                c.close()
            
            fout.close()
            
            f = xr.open_dataset(outfile, engine='cfgrib')
            f['time'] = datetime.strptime(row['forecast_date'],  '%Y%m%d%H')

            v = list(f.keys())
            var = outfile.split('/')[-1]
            var = var.split('_')[0]
            f = f.rename({v[0] : var})

            if 'step': f = f.drop_vars('step')

            if 'valid_time' in f: f = f.drop_vars('valid_time')
            
            if 'surface' in f:
                
                f = f.drop_vars('surface')

            if 'isobaricInhPa' in f:
                f = f.rename({'isobaricInhPa' : 'level'})
                f = f.expand_dims(['level'])

            if 'heightAboveGround' in f: f = f.drop_vars('heightAboveGround')

            if 'atmosphereSingleLayer' in f: f = f.drop_vars('atmosphereSingleLayer')

            if 'meanSea' in  f:
                f = f.drop_vars('meanSea')

            f = f.expand_dims(['time'])
            outnc = outfile.split('/')[-1]

            # Transforma unidade
            if var in self.dict['transform']:
                tr = float(self.dict['transform'][var][1:])
                op = self.dict['transform'][var][0]
                f = eval(f'f {op} tr')

            if 't2m' in f:
                f['t2m'].attrs['units'] = 'C'

            if 't' in f:
                f['t'].attrs['units'] = 'C'
            # self.xarray['lev'].attrs['units'] = 'hPa'
            
            if self.dict['area']['reduce'] ==  True:

                lat1 = self.dict['area']['minlat']
                lat2 = self.dict['area']['maxlat'] 
                lon1 = self.dict['area']['minlon']
                lon2 = self.dict['area']['maxlon']

            
                f2 = f.sel(latitude=slice(lat2, lat1), 
                          longitude=slice(lon1, lon2)).copy()
            else:
                f2 = f

            f2.to_netcdf(f'{pathout}/{outnc}.nc4', encoding={'time': {'dtype': 'i4'}})
            f2.close()
            f.close()
                 
        gc.collect()
        files = glob.glob(f"{pathout}/*.nc4")

        f = xr.open_mfdataset(files,  combine='nested', parallel=False,  chunks={'latitude': 150, 'longitude': 150})
        
        # Transform accumulated precipitation
        # TimeStamp 0 and 1 without modification
        if 'precip' in f:

            arr = []
            for dt in np.arange(len(f.time)):
                
                if dt <= 1:
                    arr.append(f.isel(time=dt)[['precip']])
                else:
                    fout = f.isel(time=dt)[['precip']] - f.isel(time=dt-1)[['precip']]
                    fout = fout.assign_coords({'time': f.time[dt]})
                    fout = fout.expand_dims('time')
                    arr.append(fout)
            
            f['precip'] = xr.concat(arr, dim="time")['precip']

        f.attrs = {
                            "center" :	"National Institute for Space Research - INPE",
                            "model"  :  f"Global Forecast System  ({self.dict['model']['parameter']})"
        }
        f.time.encoding['units'] = "Seconds since 1970-01-01 00:00:00"

        field = f.load()

        if self.dict['save_netcdf'] == True:

            pathout = f"{self.dict['path_to_save']}/{self.local_path}/{self.year}/{self.mon}/{self.day}/{self.hour}"
            os.makedirs(pathout, exist_ok=True)
            ncout = self.dict['file']['name'].format(row['start_date'], row['forecast_date'])
            ncout = ncout.replace(f"{self.dict['file']['format']}","nc4")

            if os.path.exists(f"{pathout}/{ncout}"): os.remove(f"{pathout}/{ncout}")
            field.to_netcdf(f"{pathout}/{ncout}", encoding={'time': {'dtype': 'i4'}})

        f.close()

        gc.collect()
        self.file = field