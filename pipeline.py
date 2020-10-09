import logging
from urllib.parse import urlparse
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(df):

    logger.info('Elimino los registros vacíos de los campos precio (m2 y tota) y sup (cubierta y total)')
    df = df.dropna(axis = 0, subset=['price_aprox_usd','price_usd_per_m2','surface_covered_in_m2','surface_total_in_m2'])
    
    logger.info('Completo los NaN de los rooms con el promedio de los registors')
    rooms_mean = {'rooms': df.rooms.mean()}
    df = df.fillna(value=rooms_mean).reset_index(drop=True)

    logger.info('Extraigo la Zona')
    df['Zona'] = df.place_with_parent_names.apply(lambda x : x.split('|')[2])


    logger.info('Elimino columnas que no voy a usar')
    df = df.drop(labels=['created_on','operation','place_with_parent_names',
                     'properati_url','comuna','lat-lon','lat','lon', 'floor', 'expenses'], axis=1)
    

    logger.info('Control de inconsistencias entre sup_total vs sup_cubiertas')
    wrong_surface = df[df['surface_covered_in_m2'] > df['surface_total_in_m2']]
    df.at[wrong_surface.index, 'surface_total_in_m2'] = wrong_surface.surface_covered_in_m2
    df.at[wrong_surface.index, 'surface_covered_in_m2'] = wrong_surface.surface_total_in_m2

    return df
    
if __name__ == '__main__':


    df = main(df)
