package com.example.springdemo.pojo;

import jakarta.persistence.*;

@Table(name = "tb_record")
@Entity
public class Record {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "record_id")
    private int id;

    @Column(name = "record_time")
    private String time;

    @Column(name = "record_person")  // 当前人数
    private int person;

    @Column(name = "record_reserved_person")  // 已预约人数
    private int reservedPerson;

    @Column(name = "record_restaurant_id")
    private int res_id;  // 所属的餐厅号

    public Record() {}

    public Record(int id, String time, int person, int reservedPerson, int res_id) {
        this.id = id;
        this.time = time;
        this.person = person;
        this.reservedPerson = reservedPerson;
        this.res_id = res_id;
    }

    // Getter 和 Setter

    public int getId() {
        return id;
    }

    public String getTime() {
        return time;
    }

    public int getPerson() {
        return person;
    }

    public int getReservedPerson() {
        return reservedPerson;
    }

    public int getRes_id() {
        return res_id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public void setPerson(int person) {
        this.person = person;
    }

    public void setReservedPerson(int reservedPerson) {
        this.reservedPerson = reservedPerson;
    }

    public void setRes_id(int res_id) {
        this.res_id = res_id;
    }

    @Override
    public String toString() {
        return "Record{" +
                "id=" + id +
                ", time='" + time + '\'' +
                ", person=" + person +
                ", reservedPerson=" + reservedPerson +
                ", res_id=" + res_id +
                '}';
    }
}
