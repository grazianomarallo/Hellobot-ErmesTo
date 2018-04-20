package com.grazianomarallo.RestfulService;


import com.grazianomarallo.RestfulService.Cafeteria.Cafeteria;
import com.grazianomarallo.RestfulService.Studyroom.StudyRoom;

import java.util.concurrent.ConcurrentHashMap;

/**
 * Created by grazianomarallo on 11/11/2017.
 */
public class MyMap {

    private static java.util.Map<String, Cafeteria> cafeterias = new ConcurrentHashMap<String, Cafeteria>();
    private static java.util.Map<String, StudyRoom> studyRooms = new ConcurrentHashMap<>();


    public static java.util.Map<String, Cafeteria> getCafeteria() {
        return cafeterias;
    }




}


