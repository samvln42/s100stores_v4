import Header from "../header/Header";
import Menu from "../menuFooter/Menu";
import { IoIosArrowBack } from "react-icons/io";
import "./bill.css";
import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import ReviewProduct from "./ReviewProduct";
import productImage from "../../img/productImage.png";

const Bill = () => {
  const token = localStorage.getItem("token");
  const order_id = useParams().bill_id;
  const [order_list, setOrderList] = useState("");
  var totalPrice = 0;
  const [showReview, setShowReview] = useState(false);
  const [product_id, set_product_id] = useState(null);

  const navigate = useNavigate();

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
    const config = {
      method: "get",
      maxBodyLength: Infinity,
      url: import.meta.env.VITE_API + `/store/order/${order_id}`,
      headers: {
        "Content-Type": "application/json",
      },
    };

    axios
      .request(config)
      .then((response) => {
        setOrderList(response.data);
      })
      .catch((error) => {
        console.error("Error fetching products:", error);
      });
  }, [order_id]);

  const handleReview = (id) => {
    set_product_id(id);
    setShowReview(true);
  };

  return (
    <>
      {showReview ? (
        <ReviewProduct id={product_id} />
      ) : (
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
                  <p>Order ID: {order_list.id}</p>
                  <p>
                    Date: {new Date(order_list.created_at).toLocaleString()}
                  </p>
                  {/* <p>Name: </p> */}
                </div>
              </div>
              <div className="billGopBox">
                <table>
                  <thead>
                    <tr>
                      <th>Product</th>
                      <th>Price</th>
                      <th>Amount</th>
                      <th>Color</th>
                      <th>Size</th>
                      {order_list.status === "Delivered" && <th>Review</th>}
                    </tr>
                  </thead>
                  <tbody>
                    {order_list.items &&
                      order_list.items.map((item, index) => (
                        // console.log(item.product)

                        <tr key={index}>
                          <td>{item.product.name}</td>
                          <td>
                            {parseFloat(item.price).toLocaleString("en-US", {
                              minimumFractionDigits: 0,
                              maximumFractionDigits: 0,
                              useGrouping: true,
                            })}
                          </td>
                          <td>{item.quantity}</td>
                          <td>{item.color}</td>
                          <td>{item.size}</td>
                          {order_list.status === "Delivered" && (
                            <th>
                              <button
                              className="Delivered_review"
                                onClick={() => {
                                  handleReview(item.product.id);
                                }}
                              >
                                Review
                              </button>
                            </th>
                          )}
                          <p hidden>
                            {(totalPrice += item.price * item.quantity)}
                          </p>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
              <div className="titlePrice">
                <p>Total:</p>
                <p>
                  $
                  {parseFloat(totalPrice).toLocaleString("en-US", {
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0,
                    useGrouping: true,
                  })}{" "}
                </p>
              </div>
              <div className="box_place">
                <div className="place-on">
                  <p>Place on: BCEL</p>
                  <p>Payment method: Transfer</p>
                  <p>Contact number: +85620{order_list.tel}</p>
                  <p>Status: {order_list.status}</p>

                  <div className="Box_China_Branch">
                    <p>Follow items (China to Laos): </p>
                    <Link to={order_list.china_url}>Click here</Link>
                  </div>
                  <div className="Box_China_Branch">
                    <p>Follow items (Branch to Branch): </p>
                    <Link to={order_list.lao_url}>Click here</Link>
                  </div>
                </div>
                <div className="Box_btn_bill">
                  <img src={productImage} alt="img" />
                </div>
              </div>
            </div>
            
          </div>
          <Menu />
        </>
      )}
    </>
  );
};

export default Bill;
