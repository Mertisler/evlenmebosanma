import folium 
import json
import csv
import matplotlib.colors as mcolors

class Map():

    TURKEY_CITIES_COORDINATS_JSON_FILE = "iller.json"
    TURKEY_CITIES_MAP_FILE = "Map.html"
    TURKEY_COORDINATS_JSON = {}
    
    def CreateMap(self):
        self.turkeyMap = folium.Map(location=(39.925533, 32.866743), zoom_start=6)
        self.GetCitiesCoordinats()

    def SaveMap(self):
        folium.LayerControl().add_to(self.turkeyMap)
        self.turkeyMap.save(self.TURKEY_CITIES_MAP_FILE)

    def CreateLayout(self, groupName):
        return folium.FeatureGroup(groupName, show=False).add_to(self.turkeyMap)

    def AddMarker(self, location, popup, tooltip, icon=None, add_to=None):
        folium.Marker(
            location=location,
            popup=popup,
            tooltip=tooltip,
            icon=icon
        ).add_to(add_to)

    def GetCitiesCoordinats(self):
        with open(self.TURKEY_CITIES_COORDINATS_JSON_FILE, "r", encoding="utf-8") as file:
            self.TURKEY_COORDINATS_JSON = json.load(file)

    def PlaceAllCity(self, layout, csvFilePath, Markers=True, Edges=True):

        def create_colormap():
            colors = ["#8B0000", "#FF0000", "#FF4500", "#FFD700", "#ADFF2F", "#7FFF00", "#00FF00"]
            return mcolors.LinearSegmentedColormap.from_list("custom_gradient", colors, N=81)

        def getColor(index, total):
            colormap = create_colormap()
            hexCode = mcolors.to_hex(colormap(index / (total - 1)))
            return hexCode

        data = self.ReadCSV(csvFilePath)
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        
        total_cities = len(sorted_data)
        cityColors = {city: getColor(index, total_cities) for index, (city, _) in enumerate(sorted_data)}

        for i in range(total_cities - 1):
            start_city = sorted_data[i][0]
            end_city = sorted_data[i + 1][0]
            start_loc = self.TURKEY_COORDINATS_JSON[start_city]
            end_loc = self.TURKEY_COORDINATS_JSON[end_city]
            start_color = cityColors[start_city]
            end_color = cityColors[end_city]

            color_gradient = mcolors.LinearSegmentedColormap.from_list("custom", [start_color, end_color])
            line_color = mcolors.to_hex(color_gradient(0.5))

            folium.PolyLine(locations=[start_loc, end_loc], color=line_color, weight=3).add_to(layout)

        for city, coordinatOfCity in self.TURKEY_COORDINATS_JSON.items():
            if city in cityColors:
                self.AddMarker(coordinatOfCity, popup=None, tooltip=f"{city}\n{data[city]}", icon=folium.Icon(color="white", icon_color=cityColors[city]), add_to=layout)

    @staticmethod
    def ReadCSV(csvFile):
        city_dict = {}
        with open(csvFile, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                city = row[0]
                value = int(row[1])
                match city:
                    case "Aydin":
                        city = "Aydın"
                    case "Ağri":
                        city = "Ağrı"
                    case "Balikesir":
                        city = "Balıkesir"
                    case "Bartin":
                        city = "Bartın"
                    case "Iğdir":
                        city = "Iğdır"
                    case "Kirklareli":
                        city = "Kırklareli"
                    case "Kirikkale":
                        city = "Kırıkkale"
                    case "Kirsehir":
                        city = "Kırşehir"
                    case _:
                        city = city

                city_dict[city] = value

        return city_dict
