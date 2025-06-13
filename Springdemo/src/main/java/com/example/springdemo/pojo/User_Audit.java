package com.example.springdemo.pojo;

import jakarta.persistence.*;

@Table(name = "tb_audit")
@Entity
public class User_Audit {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "audit_id" )
    private Integer audit_id;
    @ManyToOne(cascade = CascadeType.PERSIST)
    private User applicant;
    @Column(name = "handled" )
    private boolean handled = false; // 是否已处理

    public User_Audit(){}
    public User_Audit(Integer audit_id, User applicant) {
        this.audit_id = audit_id;
        this.applicant = applicant;
    }

    @Override
    public String toString() {
        return "User_Audit{" +
                "audit_id=" + audit_id +
                ", applicant=" + applicant +
                '}';
    }


    public void setHandled(boolean handled) {
        this.handled = handled;
    }

    public boolean isHandled() {
        return handled;
    }

    public void setAudit_id(Integer audit_id) {
        this.audit_id = audit_id;
    }

    public void setApplicant(User applicant) {
        this.applicant = applicant;
    }

    public Integer getAudit_id() {
        return audit_id;
    }

    public User getApplicant() {
        return applicant;
    }
}
