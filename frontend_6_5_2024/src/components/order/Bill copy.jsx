import Header from "../header/Header";
import Menu from "../menuFooter/Menu";
import { IoIosArrowBack } from "react-icons/io";
import "./bill.css";
import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { format } from "date-fns";
import axios from "axios";

const Bill = () => {
  const token = localStorage.getItem("token");
  const order_id = useParams().bill_id;
  const [order_list, set_order_list] = useState([]);
  var totalPrice = 0;

  // console.log("order id", order_id);
  console.log(order_list);

  const navigate = useNavigate();

  // useEffect(() => {
  //   let data = JSON.stringify({
  //     token: token,
  //   });

  //   let config = {
  //     method: "post",
  //     maxBodyLength: Infinity,
  //     url: import.meta.env.VITE_API + "/user/check-token",
  //     headers: {
  //       "Content-Type": "application/json",
  //       Authorization: "Bearer " + token,
  //     },
  //     data: data,
  //   };

  //   axios
  //     .request(config)
  //     .then((response) => {
  //       if (response.data.result != "success") {
  //         localStorage.clear();
  //         navigate("/loginuser");
  //         return;
  //       }
  //     })
  //     .catch((error) => {
  //       localStorage.clear();
  //       console.log(error);
  //       navigate("/loginuser");
  //       return;
  //     });
  // }, [token]);

  useEffect(() => {
    const config = {
      method: "get",
      maxBodyLength: Infinity,
      url: import.meta.env.VITE_API + `/api/order/${order_id}`,
      headers: {
        "Content-Type": "application/json",
      },
    };

    axios
      .request(config)
      .then((response) => {
        set_order_list(response.data);
      })
      .catch((error) => {
        console.error("Error fetching products:", error);
      });
  }, [order_id]);



  




  // Convert the price string to a number
  const price = parseFloat(order_list.price);

  // Format the price with commas as thousands separators and fixed decimal places
  const formattedPrice = price.toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
    useGrouping: true, // Add commas as thousands separators
  });

  return (
    <>
      <Header></Header>
      <div className="bill">
        <Link to="/order" className="box_container_back_icons_back">
          <IoIosArrowBack id="icons_back" />
          <p>Back</p>
        </Link>
        <div className="bill-detial newspanBox">
          <div className="guopoidHead">
            <div className="idf">
              <p>OrderID: {order_list.id}</p>
              <p>Date: {new Date(order_list.created_at).toLocaleString()}</p>
              {/* <p>Name: </p> */}
            </div>
          </div>
          <div className="billGopBox">
            <table>
              <thead>
                <tr>
                  <th>Product Name</th>
                  <th>Price</th>
                  <th>Amount</th>
                  <th>Color</th>
                  <th>Size</th>
                </tr>
              </thead>
              <tbody>
                {
                  order_list.items &&
                    order_list.items.map((item, index) => (
                      
                      // console.log(item.product)
                      <tr key={index}>
                        <td>{item.product}</td>
                        <td>
                          {parseFloat(item.price).toLocaleString("en-US", {
                            minimumFractionDigits: 0,
                            maximumFractionDigits: 0,
                            useGrouping: true,
                          })
                          
                          }
                        </td>
                        <td>{item.quantity}</td>
                        <td>{item.color}</td>
                        <td>{item.size}</td>
                        <p hidden>{totalPrice = item.price*item.quantity}</p>
                      </tr>
                    ))
                }
              </tbody>
            </table>
          </div>
          <div className="titlePrice">
            <p>Total:</p>
            <p>
              {parseFloat(totalPrice).toLocaleString("en-US", {
                minimumFractionDigits: 0,
                maximumFractionDigits: 0,
                useGrouping: true,
              })} Kip
            </p>
          </div>
          <div className="place-on">
            <p>Place on: BCEL</p>
            <p>Payment method: Transfer</p>
            <p>Contact number: +85620{order_list.tel}</p>
            <p>Status: {order_list.status}</p>
            <p>Delivery: {order_list.shipping_company}, Province: {order_list.province}, Destrict: {order_list.district}, Branch: {order_list.branch}</p>
          </div>
        </div>
      </div>
      <Menu />
    </>
  );
};

export default Bill;
