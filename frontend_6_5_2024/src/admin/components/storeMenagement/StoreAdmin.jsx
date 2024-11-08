import React, { useEffect, useState } from "react";
import "./storeAdmin.css";
import { IoSearchOutline } from "react-icons/io5";
import AdminMenu from "../adminMenu/AdminMenu";
import { Link, useNavigate } from "react-router-dom";
import { BiPlus } from "react-icons/bi";
import profile from "../../../img/profile.jpg";
import axios from "axios";

function StoreAdmin() {
  const token = localStorage.getItem("token");
  const navigate = useNavigate();
  const [stores, set_stores] = useState([]);

  useEffect(() => {
    let data = JSON.stringify({
      token: token,
    });

    let config = {
      method: "post",
      maxBodyLength: Infinity,
      url: import.meta.env.VITE_API + "/user/check-token",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      data: data,
    };

    axios
      .request(config)
      .then((response) => {
        console.log(response.data);
        if (response.data.result != "success") {
          localStorage.clear();

          navigate("/loginuser");
          return;
        }
      })
      .catch((error) => {
        localStorage.clear();
        console.log(error);
        navigate("/loginuser");
        return;
      });
  }, [token]);

  useEffect(() => {
    let config = {
      method: "get",
      maxBodyLength: Infinity,
      url: import.meta.env.VITE_API + "/store/all-stores",
      headers: {
        "Content-Type": "application/json",
      },
    };

    axios
      .request(config)
      .then((response) => {
        // console.log(JSON.stringify(response.data));
        set_stores(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [stores]);

  const handleDelete = (id) => {
    let data = "";

    console.log(id);

    let config = {
      method: "delete",
      maxBodyLength: Infinity,
      url: import.meta.env.VITE_API + `/user/seller-users/${id}`,
      headers: {},
      data: data,
    };

    axios
      .request(config)
      .then((response) => {
        alert("Delete store successful.");
      })
      .catch((error) => {
        console.log(error);
      });
  };

  console.log(stores);

  return (
    <>
      <section id="menager">
        <AdminMenu />
        <div className="container_body_adminuser">
          <div className="container_box_users">
            <div className="box_users">
              {/* <div className="box_add_admin">
                <Link to="#" className="btn_addadmin">
                  <BiPlus id="icon_add_admin" />
                  Add Store
                </Link>
              </div> */}

              {/* <form className="search">
                <div className="search-box_menageruser">
                  <input type="text" placeholder="Search ..." />
                  <button type="submit">
                    <IoSearchOutline />
                  </button>
                </div>
              </form> */}
            </div>
            <div className="box_contanier_stoerNumonevb">
              {stores.length === 0 ? (
                <p className="no-reviews-message">No Order</p>
              ) : (
                stores.map((store, index) => (
                  <div className="box_contanier_stoer" key={index}>
                    <p>{store.name}</p>
                    <p>{store.address}</p>
                    <div className="btn_box_Cont">
                      <button
                        className="delete_storeDetails"
                        onClick={() => {
                          handleDelete(store.seller.id);
                        }}
                      >
                        Delete
                      </button>
                      <button className="viewMore_storeDetails">View</button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export default StoreAdmin;
