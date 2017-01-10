#!/usr/bin/env/python

import json
import urllib2
import time
import os

def get_weather(current_time, cache_file) :
	json_weather = json.load(urllib2.urlopen("http://api.openweathermap.org/data/2.5/forecast/city?id=498817&APPID=c086afd9bcc37005069b8e6d2dcc3ba2a"));
	
	element = 0;
	
	while json_weather["list"][element]["dt"] < current_time :
		element += 1;
	
	current_weather = json_weather["list"][element];

	dt = current_weather["dt"];	
	
	kelvin = 273.15;
	temp = current_weather["main"]["temp"] - kelvin; 
	
	wind = current_weather["wind"]["speed"];
	
	desc = current_weather["weather"][0]["description"]; 
	
	result_string = "Current temperature is " + str(temp) + " degrees, wind is " + str(wind) + " meters per second, it is " + desc + " outside.";
	
	json_data = {
		"dt" : dt,
		"value" : result_string,
	}	
	
	with open(cache_file, 'w') as file :
		json.dump(json_data, file);
	return result_string;

get_new = False;
cache_dir = "./.cache";
cache_file = "./.cache/weather";
current_time = time.time();

if (not os.path.isdir(cache_dir)) :
	os.makedirs(cache_dir);
	get_new = True;

if (not get_new and os.path.isfile(cache_file)) :
	with open(cache_file, 'r') as file :
		cache = json.load(file);

	if (cache["dt"] > current_time) : 
		result = cache["value"];
	else :
		get_new = True;
else :
	get_new = True;

if (get_new) :
	result = get_weather(current_time, cache_file);

print result;
