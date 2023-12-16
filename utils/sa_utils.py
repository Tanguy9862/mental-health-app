import pandas as pd


def filter_on_continent(df, continent):
    return df.query("Continent == @continent")


def filter_on_entity(df, entity):
    return df.query("Entity in @entity")

