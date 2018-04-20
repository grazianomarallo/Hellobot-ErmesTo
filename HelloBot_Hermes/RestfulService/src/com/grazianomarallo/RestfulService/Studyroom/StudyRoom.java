package com.grazianomarallo.RestfulService.Studyroom;

import com.grazianomarallo.RestfulService.BaseInfo;
import com.grazianomarallo.RestfulService.Resource;


/**
 * Created by grazianomarallo on 12/11/2017.
 */
public class StudyRoom extends Resource{

    private BaseInfo info;



    public StudyRoom(int capacity, BaseInfo informations) {
        super(capacity, informations);
        this.info = informations;
    }


    public BaseInfo getInfo() {
        return info;
    }

    public void setInfo(BaseInfo info) {
        this.info = info;
    }
}
