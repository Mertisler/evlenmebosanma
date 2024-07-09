from map import Map
import os

def GetFiles(directory_path):
    items = os.listdir(directory_path)
    
    # Sadece dosyaları filtrele
    files = [item for item in items if os.path.isfile(os.path.join(directory_path, item))]
    
    return files

if __name__ =="__main__":
    map = Map()
    map.CreateMap()
    
    for file in GetFiles("datas"):
        file:str
        year = file[:file.index(".")]
        layout= map.CreateLayout(year)
        map.PlaceAllCity(layout,"datas/"+file,Markers=True,Edges=True)
    map.SaveMap()