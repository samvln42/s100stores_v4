import React, { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import "./productDetails.css";
import Header from "../header/Header";
import Menu from "../menuFooter/Menu";
import Payment from "../cart/Payment";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";
import { RotatingLines } from "react-loader-spinner";

import { IoIosArrowBack } from "react-icons/io";
import { BiStore } from "react-icons/bi";
import icon_star from "../../img/icon_star.png";
import icon_star2 from "../../img/icon_star2.png";
import user from "../../img/user.png";
import productImage from "../../img/productImage.png";
import detailproduct from "../../img/detailproduct.jpg";
import axios from "axios";
import { ToggleButtonGroup, ToggleButton } from "@mui/material";
import { FaLocationDot } from "react-icons/fa6";
import { set } from "date-fns";

function ProductDetails() {
  const token = localStorage.getItem("token");
  const user = localStorage.getItem("user");
  const [store_id, set_store_id] = useState([]);
  const navigate = useNavigate();
  const product_id = useParams().goods_id;
  const [products_list, set_products_list] = useState([]);
  const [reiews_list, set_reviews_list] = useState([]);
  const [sliceNum, set_sliceNum] = useState(8);
  const [category, set_category] = useState(1);
  const storage = JSON.parse(window.localStorage.getItem("user"));

  const [showPayment, setShowPayment] = useState(false);
  const [product, setProduct] = useState(null);
  const [price, set_price] = useState(null);
  const MySwal = withReactContent(Swal);

  //Active sizes
  const [sizes, setSizes] = useState([]);
  const [activeIndex, setActiveIndex] = useState(0);

  const extractSizeNames = (data) => {
    if (data && data.sizes) {
      const sizeNames = data.sizes.map((size) => size.name);
      setSizes(sizeNames);
    }
  };
  const handleSizeClick = (index) => {
    setActiveIndex(index);
    set_size(sizes[index]);
  };

  //Active color
  const [colors, setColors] = useState([]);
  const [activeColorIndex, setActiveColorIndex] = useState(0);

  const extractColorNames = (data) => {
    if (data && data.colors) {
      const colorNames = data.colors.map((color) => color.name);
      setColors(colorNames);
    }
  };
  const handleColorClick = (index) => {
    setActiveColorIndex(index);
    set_color(colors[index]);
  };

  // console.log(sizes);

  const [size, set_size] = useState(null);
  const [color, set_color] = useState(null);
  const [quantity, set_quantity] = useState(1);

  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState("");
  const [reviews, setReviews] = useState([]);
  const [displayedReviews, setDisplayedReviews] = useState([]);
  const [showAllReviews, setShowAllReviews] = useState(false);

  var user_id = null;
  if (localStorage.getItem("user")) {
    user_id = JSON.parse(window.localStorage.getItem("user")).user_id;
  }

  const [order, setOrder] = useState([]);

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
      url: import.meta.env.VITE_API + `/store/detail/${product_id}`,
      headers: {
        "Content-Type": "application/json",
      },
    };

    axios
      .request(config)
      .then((response) => {
        setProduct(response.data);
        extractSizeNames(response.data);
        extractColorNames(response.data);
        set_price(response.data.price);
        set_store_id(response.data.store_id);

        if (response.data.sizes && response.data.sizes.length > 0) {
          set_size(response.data.sizes[0].name);
        }
        if (response.data.colors && response.data.colors.length > 0) {
          set_color(response.data.colors[0].name);
        }
      })
      .catch((error) => {
        console.error("Error fetching products:", error);
      });
  }, [product_id]);

  useEffect(() => {
    let config = {
      method: "get",
      maxBodyLength: Infinity,
      url: import.meta.env.VITE_API + `/store/?category=${category}`,
      headers: {
        "Content-Type": "application/json",
      },
    };

    axios
      .request(config)
      .then((response) => {
        set_products_list(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [category]);

  // const handleSizeClick = (sizeName) => {
  //   // set_size(size === sizeName ? null : sizeName);
  //   set_size(sizeName);
  // };

  // const handleColorClick = (colorName) => {
  //   // set_color(color === colorName ? null : colorName);
  //   set_color(colorName);
  // };

  const decrease = () => {
    if (quantity > 1) {
      set_quantity(quantity - 1);
    }
  };

  const increase = () => {
    set_quantity(quantity + 1);
  };

  // ============= Cart management ================
  const [cart, setCart] = useState(() => {
    const localCart = localStorage.getItem("cart");
    return localCart ? JSON.parse(localCart) : [];
  });

  useEffect(() => {
    localStorage.setItem("cart", JSON.stringify(cart));
  }, [cart]);

  const addToCart = (product, color, size, quantity) => {
    if (color == null) {
      alert("Please select the color");
      return; // Abort the function if color is null
    }
    if (size == null) {
      alert("Please select the size");
      return; // Abort the function if color is null
    }

    const existingProduct = cart.find(
      (item) =>
        item.id === product.id &&
        item.store_name === product.store_name &&
        item.color === color &&
        item.size === size
    );

    if (existingProduct) {
      setCart(
        cart.map((item) =>
          item.id === product.id &&
          item.store_name === product.store_name &&
          item.color === color &&
          item.size === size
            ? { ...item, quantity: item.quantity + quantity }
            : item
        )
      );
    } else {
      setCart([...cart, { ...product, quantity, color, size }]);
    }

    // alert("This product has been added to cart.");

    MySwal.fire({
      text: "This product has been added to cart.",
      icon: "success",
    });

    // set_color(null);
    // set_size(null);
    // set_quantity(1);
  };

  useEffect(() => {
    let data = "";

    let config = {
      method: "get",
      maxBodyLength: Infinity,
      url: import.meta.env.VITE_API + `/store/product/${product_id}/review`,
      headers: {
        "Content-Type": "application/json",
      },
      data: data,
    };

    axios
      .request(config)
      .then((response) => {
        const sortedReviews = response.data.sort((a, b) => b.id - a.id);
        setReviews(sortedReviews);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [product_id]);

  // Update displayed reviews when the reviews or showAllReviews state changes
  useEffect(() => {
    if (showAllReviews) {
      setDisplayedReviews(reviews);
    } else {
      setDisplayedReviews(reviews.slice(0, 3));
    }
  }, [reviews, showAllReviews]);

  const handleToggleReviews = () => {
    setShowAllReviews(!showAllReviews);
  };

  function StarAVG(value) {
    let star_avg = (value / 5) * 100;
    if (star_avg === 0) {
      star_avg = 100;
    }
    return star_avg;
  }

  const handlePay = (product, color, size, quantity) => {
    // if (!color) {
    //   alert("Please select the color");
    //   return; // Abort the function if color is null
    // }
    // if (!size) {
    //   alert("Please select the size");
    //   return; // Abort the function if color is null
    // }
    setOrder([
      {
        user: user_id,
        store: store_id,
        items: [
          {
            id: product.id,
            name: product.name,
            images: product.images,
            quantity: quantity,
            price: price,
            color: color,
            size: size,
          },
        ],
      },
    ]);
    setShowPayment(true);
  };

  return (
    <>
      {showPayment ? (
        <Payment orders={order} order_from="buy_now" onPay={handlePay} />
      ) : (
        <>
          <Header />
          <div className="contentBody">
            <div className="box_betavinOfob">
              {product ? (
                <div>
                  <form className="boxProduct_deteils">
                    <div className="product-page-img">
                      <img src={`${import.meta.env.VITE_API}/${product.images}`} alt="" />
                    </div>
                    <div className="txtContentproduct">
                      <h1 className="txt_nameP">{product.name}</h1>
                      <p className="money_txt">$ {product.format_price}</p>
                      
                      <p className="txt_description">{product.description}</p>

                      <div className="star">
                        <div
                          className="on"
                          style={{ width: `${StarAVG(product.star_avg)}%` }}
                        ></div>
                      </div>

                      <div className="size_product">
                        <p>Color:</p>
                        {product.colors && (
                          <div className="size">
                            {colors.map((color, index) => (
                              <p
                                key={index}
                                className={
                                  index === activeColorIndex
                                    ? "active echSize"
                                    : "echSize"
                                }
                                onClick={() => handleColorClick(index)}
                              >
                                {color}
                              </p>
                            ))}
                          </div>
                        )}
                      </div>

                      <div className="size_product">
                        <p>Size:</p>
                        {product.sizes && (
                          <div className="size">
                            {sizes.map((size, index) => (
                              <p
                                key={index}
                                className={
                                  index === activeIndex
                                    ? "active echSize"
                                    : "echSize"
                                }
                                onClick={() => handleSizeClick(index)}
                              >
                                {size}
                              </p>
                            ))}
                          </div>
                        )}
                      </div>

                      <div className="container_item_icon">
                        <div
                          className="container_minus_plus"
                          onClick={decrease}
                        >
                          -
                        </div>
                        <span>{quantity}</span>
                        <div
                          className="container_minus_plus"
                          onClick={increase}
                        >
                          +
                        </div>
                      </div>
                      <div className="Count_product">
                        <Link
                          className="echbtn btnBut"
                          onClick={() => {
                            handlePay(product, color, size, quantity);
                          }}
                        >
                          {/* <Link className="echbtn btnBut" to={"/payment"}> */}
                          Buy Now
                        </Link>
                        <Link
                          className="echbtn btnAdd"
                          onClick={() =>
                            addToCart(product, color, size, quantity)
                          }
                        >
                          Add To Cart
                        </Link>
                      </div>
                    </div>
                  </form>
                </div>
              ) : (
                // <p>Loading...</p>
                <div className="box_RotatingLines">
                  <RotatingLines
                    visible={true}
                    height="45"
                    width="45"
                    color="grey"
                    strokeWidth="5"
                    animationDuration="0.75"
                    ariaLabel="rotating-lines-loading"
                    wrapperStyle={{}}
                    wrapperClass=""
                  />
                </div>
              )}

              <div className="review-list">
                <h2 className="review-list-title">All Reviews</h2>
                {displayedReviews.length === 0 ? (
                  <p className="no-reviews-message">No reviews available</p>
                ) : (
                  <ul className="reviews">
                    {displayedReviews.map((review) => (
                      <li key={review.id} className="review-item">
                        <h3 className="rating">
                          {review.user.nickname || "null"}:
                        </h3>
                        <p className="comment">{review.comment || "null"}</p>
                        {/* Display other review details as needed */}
                      </li>
                    ))}
                  </ul>
                )}
                {reviews.length > 3 && (
                  <button
                    className="toggle-reviews-button"
                    onClick={handleToggleReviews}
                  >
                    {showAllReviews ? "Show Less" : "Show More"}
                  </button>
                )}
              </div>
            </div>
            <h2 className="box_betavinOfob asd2">
              <span className="spennofStyle"> </span>
              More products
            </h2>
            <div className="product-area">
              {products_list.map(
                (i, index) =>
                  i.category !== "Food" && (
                    <div className="box-product" key={index}>
                      <Link to={"/goods/" + i.id}>
                        <div className="img">
                          <img src={`${import.meta.env.VITE_API}/${i.images}`} alt="image" />
                        </div>
                        <div className="star">
                          <div
                            className="on"
                            style={{ width: `${StarAVG(i.star_avg)}%` }}
                          ></div>
                        </div>
                        <ul className="txtOFproduct2">
                          <li className="name">{i.name}</li>
                          <li className="price">$ {i.format_price}</li>
                          <li className="desc">{i.description}</li>
                        </ul>
                      </Link>
                    </div>
                  )
              )}
            </div>
          </div>

          <Menu />
        </>
      )}
    </>
  );
}

export default ProductDetails;
