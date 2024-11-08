import "./product_Admin.css";
import productImage from "../../../img/productImage.png";
import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import AdminMenu from "../adminMenu/AdminMenu";
import { BiPlus } from "react-icons/bi";
import { MdOutlineEdit } from "react-icons/md";
import { CiCamera } from "react-icons/ci";
import imageicon from "../../../img/imageicon.jpg";
import banner_no from "../../../img/banner_no.jpg";
import { AiOutlineDelete } from "react-icons/ai";
import axios from "axios";
import { MdClose } from "react-icons/md";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";

const Product_Admin = () => {
  const token = localStorage.getItem("token");
  const user = localStorage.getItem("user");
  const storage = JSON.parse(window.localStorage.getItem("user"));
  const [filter, set_filter] = useState(1);
  const [category_name, set_category_name] = useState("All");
  const [categories, set_categories] = useState([]);
  const navigate = useNavigate();
  const [background_image, set_background_image] = useState(null);
  const [goods_list, set_goods_list] = useState([]);

  console.log("goods_list...:", goods_list);

  const [id, set_id] = useState(null);
  const [data, set_data] = useState(null);
  const [data_array, set_data_array] = useState([]);
  const [data_color, setData_color] = useState([]);

  const [sizes, setSizes] = useState([]);
  const [colors, setColors] = useState([]);
  const [currentSize, setCurrentSize] = useState("");
  const [currentColor, setCurrentColor] = useState("");

  const MySwal = withReactContent(Swal);

  /////////////////////// Add Sizes
  useEffect(() => {
    const extractedNames = data_array.map((item) => item.name);
    setSizes(extractedNames);
  }, [data_array]);

  const handleSizeInputChange = (e, index) => {
    const { value } = e.target;
    const updatedSizes = [...sizes];
    updatedSizes[index] = value;
    setSizes(updatedSizes);
  };

  const addSizeInput = () => {
    if (currentSize.trim() !== "") {
      setSizes([...sizes, currentSize]);
      setCurrentSize("");
    }
  };

  const removeSizeInput = (sizeIndex) => {
    const updatedSizes = [...sizes];
    updatedSizes.splice(sizeIndex, 1);
    setSizes(updatedSizes);
  };
  /////////////////////// Add Colors
  useEffect(() => {
    const extractedNames = data_color.map((item) => item.name);
    setColors(extractedNames);
  }, [data_color]);

  const handleColorInputChange = (e, index) => {
    const { value } = e.target;
    const updatedColors = [...colors];
    updatedColors[index] = value;
    setColors(updatedColors);
  };

  const addColorInput = () => {
    if (currentColor.trim() !== "") {
      setColors([...colors, currentColor]);
      setCurrentColor("");
    }
  };

  const removeColorInput = (index) => {
    const updatedColors = [...colors];
    updatedColors.splice(index, 1);
    setColors(updatedColors);
  };
  var store_id = false;
  if (localStorage.getItem("user")) {
    store_id = JSON.parse(window.localStorage.getItem("user")).store_id;
  }

  const [selectedImages, setSelectedImages] = useState(null);
  const [updateProductId, setUpdateProductId] = useState(null);
  const [isConfirmationPopupOpen, setConfirmationPopupOpen] = useState(false);
  const [isConfirmationPopupOpenPrice, setConfirmationPopupOpenPrice] =
    useState(false);
  const [isConfirmationPopupOpenCategory, setConfirmationPopupOpenCategory] =
    useState(false);
  const [isConfirmationDesc, setConfirmationDesc] = useState(false);
  const [isConfirmationSize, setConfirmationSize] = useState(false);
  const [isConfirmationColor, setConfirmationColor] = useState(false);
  const [isConfirmationPopupOpenImage, setConfirmationPopupOpenImage] =
    useState(false);
  const [mainImageBanner, setMainImageBanner] = useState(null);
  const [mainImageCategory, setMainImagCategory] = useState(null);

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
    let my_url = "";
    if (category_name === "All") {
      my_url = `/store/?store_id=${store_id}`;
    } else {
      my_url = `/store/?category_name=${category_name}&category_type=${filter}`;
    }
    let config = {
      method: "get",
      maxBodyLength: Infinity,
      url: import.meta.env.VITE_API + `/store/?store_id=${store_id}`,
      headers: {
        "Content-Type": "application/json",
      },
    };

    axios
      .request(config)
      .then((response) => {
        set_goods_list(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [goods_list, category_name, filter]);

  useEffect(() => {
    let config = {
      method: "get",
      maxBodyLength: Infinity,
      url: import.meta.env.VITE_API + "/store/web-info",
      headers: {},
    };

    axios
      .request(config)
      .then((response) => {
        console.log(JSON.stringify(response.data));
        set_background_image(response.data[0].background);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [background_image]);

  useEffect(() => {
    let config = {
      method: "get",
      maxBodyLength: Infinity,
      url: import.meta.env.VITE_API + "/store/categories",
      headers: {
        "Content-Type": "application/json",
      },
    };

    axios
      .request(config)
      .then((response) => {
        // console.log(JSON.stringify(response.data));
        set_categories(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [categories]);

  console.log(background_image);

  const handleImage = (e) => {
    const file = e.target.files[0];
    set_data(file);
  };

  ///Choose image handleImageBanner
  const handleImageBanner = (e) => {
    const file = e.target.files[0];
    set_data(file);
  };

  ///Choose image handleImageProductCategory
  const handleImageProductCategory = (e) => {
    const file = e.target.files[0];
    set_data(file);
  };

  //// onClick icon edit product name
  const openConfirmationPopup = (id) => {
    // setUpdateProductId(productID.productName);
    set_id(id);
    setConfirmationPopupOpen(true);
  };

  const closeConfirmationPopup = () => {
    // setUpdateProductId(null);
    set_data(null);
    set_id(null);
    setConfirmationPopupOpen(false);
  };

  //// onClick icon camera product image
  const openConfirmationPopupImage = (id) => {
    // setUpdateProductId(productID.images);
    set_id(id);
    setConfirmationPopupOpenImage(true);
  };

  const closeConfirmationPopupImage = () => {
    // setUpdateProductId(null);
    set_data(null);
    set_id(null);
    setConfirmationPopupOpenImage(false);
    setSelectedImages(null);
  };

  ///// onClick icon edit product price

  const openConfirmationPopupPrice = (id) => {
    // setUpdateProductId(productID.price);
    set_id(id);
    setConfirmationPopupOpenPrice(true);
  };

  const closeConfirmationPopupPrice = () => {
    // setUpdateProductId(null);
    set_data(null);
    set_id(null);
    setConfirmationPopupOpenPrice(false);
  };

  ///// onClick icon edit product category

  const openConfirmationPopupCategory = (id) => {
    // setUpdateProductId(productID.price);
    set_id(id);
    setConfirmationPopupOpenCategory(true);
  };

  const closeConfirmationPopupCategory = () => {
    // setUpdateProductId(null);
    set_data(null);
    set_id(null);
    setConfirmationPopupOpenCategory(false);
  };

  ///// onClick icon edit product Desc

  const openConfirmationDesc = (id) => {
    // setUpdateProductId(productID.price);
    set_id(id);
    setConfirmationDesc(true);
  };

  const closeConfirmationDesc = () => {
    // setUpdateProductId(null);
    set_data(null);
    set_id(null);
    setConfirmationDesc(false);
  };

  ///// onClick icon edit product Size

  const openConfirmationSize = (id, sizes) => {
    // setUpdateProductId(productID.price);
    set_id(id);
    set_data_array(sizes);
    setConfirmationSize(true);
  };

  const closeConfirmationSize = () => {
    // setUpdateProductId(null);

    setConfirmationSize(false);
    set_data(null);
    set_id(null);
    setCurrentSize(null);
    set_data_array([]);
  };

  ///// onClick icon edit product Size

  const openConfirmationColor = (id, colors) => {
    // setUpdateProductId(productID.price);
    setData_color(colors);
    set_id(id);
    setConfirmationColor(true);
  };

  const closeConfirmationColor = () => {
    // setUpdateProductId(null);
    setColors([]);
    set_data(null);
    set_id(null);
    setCurrentColor(null);
    setConfirmationColor(false);
  };

  // Choose banner image
  const [isPopupimage, setPopupimage] = useState(false);

  const togglePopupimage = () => {
    setPopupimage(true);
  };

  const togglePopupCancelimage = () => {
    setPopupimage(false);
    set_data(null);
  };
  // Choose Category image
  const [isPopupName, setPopupName] = useState(false);

  const togglePopupName = (id) => {
    setPopupName(true);
    set_id(id);
  };
  const togglePopupCancelName = () => {
    setPopupName(false);
    set_id(null);
    set_data(null);
  };

  // Choose banner image
  const [isPopupImageCategory, setPopupImageCategory] = useState(false);

  const togglePopupImageCategory = (id) => {
    setPopupImageCategory(true);
    set_id(id);
  };

  const togglePopupCancelImageCategory = () => {
    setPopupImageCategory(false);
    set_id(null);
    set_data(null);
  };

  // console.log(id);
  // console.log(data);

  /////////////////////handleDelete
  const handleDelete = (id) => {
    console.log(id);
    let data = JSON.stringify({
      goods_id: id,
    });

    let config = {
      method: "delete",
      maxBodyLength: Infinity,
      url: import.meta.env.VITE_API + `/store/goods`,
      headers: {
        "Content-Type": "application/json",
      },
      data: data,
    };

    axios
      .request(config)
      .then((response) => {
        console.log(JSON.stringify(response.data));
        MySwal.fire({
          text: "Successful delete the product.",
          icon: "success",
        });
      })
      .catch((error) => {
        console.log(error);
      });
  };

  // Submit button
  const ChangeBackgroundImage = (e) => {
    e.preventDefault();
    const formdata = new FormData();
    formdata.append("background", data);

    const requestOptions = {
      method: "PATCH",
      body: formdata,
      redirect: "follow",
    };

    fetch(import.meta.env.VITE_API + `/store/web-info/2`, requestOptions)
      .then((response) => response.text())
      .then((result) => {
        console.log(result);
        MySwal.fire({
          text: "Update image banner successful.",
          icon: "success",
        });
        set_data(null);
        set_id(null);
        setPopupimage(false);
        window.location.reload(false);
      })
      .catch((error) => {
        console.error(error);
        alert("This image file is too large, please choice another image.");
      });
  };

  const ChangeCategoryImage = (e) => {
    e.preventDefault();
    const formdata = new FormData();
    formdata.append("image", data);

    const requestOptions = {
      method: "PATCH",
      body: formdata,
      redirect: "follow",
    };

    fetch(import.meta.env.VITE_API + `/store/categories/${id}`, requestOptions)
      .then((response) => response.text())
      .then((result) => {
        console.log(result);
        MySwal.fire({
          text: "Category image has been change.",
          icon: "success",
        });
        set_data(null);
        set_id(null);
        setPopupImageCategory(false);
      })
      .catch((error) => console.error(error));
  };

  const ChangeCategoryName = (e) => {
    e.preventDefault();

    const formdata = new FormData();
    formdata.append("name", data);

    const requestOptions = {
      method: "PATCH",
      body: formdata,
      redirect: "follow",
    };

    fetch(import.meta.env.VITE_API + `/store/categories/${id}`, requestOptions)
      .then((response) => response.text())
      .then((result) => {
        console.log(result);
        MySwal.fire({
          text: "Category name has been change.",
          icon: "success",
        });
        set_data(null);
        set_id(null);
        setPopupName(false);
      })
      .catch((error) => console.error(error));
  };

  const ChangeProductImage = (e) => {
    e.preventDefault();
    const formdata = new FormData();
    formdata.append("images", data);

    const requestOptions = {
      method: "PATCH",
      body: formdata,
      redirect: "follow",
    };

    fetch(
      import.meta.env.VITE_API + `/store/product/update/${id}`,
      requestOptions
    )
      .then((response) => response.text())
      .then((result) => {
        console.log(result);
        MySwal.fire({
          text: "Product image has been change.",
          icon: "success",
        });
        set_data(null);
        set_id(null);
        setConfirmationPopupOpenImage(false);
      })
      .catch((error) => console.error(error));
  };

  const ChangeProductName = () => {
    const formdata = new FormData();
    formdata.append("name", data);

    const requestOptions = {
      method: "PATCH",
      body: formdata,
      redirect: "follow",
    };

    fetch(
      import.meta.env.VITE_API + `/store/product/update/${id}`,
      requestOptions
    )
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
        setConfirmationPopupOpen(false);
        set_data(null);
        set_id(null);

        MySwal.fire({
          text: "Product name has been change.",
          icon: "success",
        });
      })
      .catch((error) => console.error(error));
  };

  const ChangeProductPrice = () => {
    const formdata = new FormData();
    formdata.append("price", data);

    const requestOptions = {
      method: "PATCH",
      body: formdata,
      redirect: "follow",
    };

    fetch(
      import.meta.env.VITE_API + `/store/product/update/${id}`,
      requestOptions
    )
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
        setConfirmationPopupOpenPrice(false);
        set_data(null);
        set_id(null);

        MySwal.fire({
          text: "Product price has been change.",
          icon: "success",
        });
      })
      .catch((error) => console.error(error));
  };

  const ChangeProductCategory = () => {
    const formdata = new FormData();
    formdata.append("category", data);

    const requestOptions = {
      method: "PATCH",
      body: formdata,
      redirect: "follow",
    };

    fetch(
      import.meta.env.VITE_API + `/store/product/update/${id}`,
      requestOptions
    )
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
        setConfirmationPopupOpenCategory(false);
        set_data(null);
        set_id(null);

        MySwal.fire({
          text: "Product category has been change.",
          icon: "success",
        });
      })
      .catch((error) => console.error(error));
  };

  const ChangeProductDescription = () => {
    const formdata = new FormData();
    formdata.append("description", data);

    const requestOptions = {
      method: "PATCH",
      body: formdata,
      redirect: "follow",
    };

    fetch(
      import.meta.env.VITE_API + `/store/product/update/${id}`,
      requestOptions
    )
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
        setConfirmationDesc(false);
        set_data(null);
        set_id(null);

        MySwal.fire({
          text: "Product description has been change.",
          icon: "success",
        });
      })
      .catch((error) => console.error(error));
  };

  const ChangeProductSizes = () => {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
      sizes: sizes,
    });

    const requestOptions = {
      method: "PATCH",
      headers: myHeaders,
      body: raw,
      redirect: "follow",
    };

    fetch(
      import.meta.env.VITE_API + `/store/product/update/${id}`,
      requestOptions
    )
      .then((response) => response.text())
      .then((result) => {
        setConfirmationSize(false);
        set_data(null);
        set_id(null);
        set_data_array([]);
        MySwal.fire({
          text: "Product sizes has been change.",
          icon: "success",
        });
      })
      .catch((error) => console.error(error));
  };

  const ChangeProductColors = () => {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
      colors: colors,
    });

    const requestOptions = {
      method: "PATCH",
      headers: myHeaders,
      body: raw,
      redirect: "follow",
    };

    fetch(
      import.meta.env.VITE_API + `/store/product/update/${id}`,
      requestOptions
    )
      .then((response) => response.text())
      .then((result) => {
        setConfirmationColor(false);
        setCurrentColor(null);
        set_data(null);
        set_id(null);
        set_data_array([]);
        MySwal.fire({
          text: "Product colors has been change.",
          icon: "success",
        });
      })
      .catch((error) => console.error(error));
  };

  return (
    <>
      <AdminMenu />
      <section id="product_admin">
        <div className="container_body_admin_product">
          <div className="productHead_content">
            <h1 className="htxthead">
              <span className="spennofStyleadmin"></span>Product
            </h1>
            <div className="categoryBoxfiler">
              <Link to="/addproduct-admin" className="box_add_product">
                <BiPlus id="icon_add_product" />
                <p>Add Product</p>
              </Link>
            </div>
          </div>
          <div className="banner_no_box">
            <div className="banner_no_box_image">
              <div className="img">
                {background_image ? (
                  <img src={background_image} alt="Banner" />
                ) : (
                  <img src={banner_no} alt="Banner" />
                )}
              </div>
            </div>
            {storage.is_admin === true && (
              <div className="edit_image_banner" onClick={togglePopupimage}>
                <CiCamera id="box_icon_camera" />
              </div>
            )}

            {isPopupimage && (
              <form
                className="background_addproductpopup_box"
                onSubmit={ChangeBackgroundImage}
              >
                <div className="hover_addproductpopup_box_image">
                  <div className="box_input_image">
                    <p>Edit banner image</p>
                    <label className="popup_Border_Boximagae">
                      {data ? (
                        <img src={URL.createObjectURL(data)} alt="Banner" />
                      ) : (
                        <img src={imageicon} alt="Banner" />
                      )}
                      <input
                        type="file"
                        id="img"
                        onChange={handleImageBanner}
                        required
                      />
                      <p className="box_choose_image">Choose img</p>
                    </label>
                  </div>
                  <div className="btn_foasdf">
                    <button
                      className="btn_cancel btn_addproducttxt_popup"
                      onClick={togglePopupCancelimage}
                    >
                      Cancel
                    </button>
                    <button
                      className="btn_confirm btn_addproducttxt_popup"
                      type="submit"
                    >
                      Update
                    </button>
                  </div>
                </div>
              </form>
            )}
          </div>

          <div className="box_category">
            {storage.is_admin === true
              ? categories.map((category, index) => (
                  <div className="box_contact_category">
                    <div className="img">
                      <img src={category.image} alt="img" />
                    </div>
                    <div
                      className="ChooseImage_category"
                      onClick={() => {
                        togglePopupImageCategory(category.id);
                      }}
                    >
                      <CiCamera id="iconCamera_category" />
                    </div>
                    <div className="box_icon_MdOutlineEdit">
                      <p>{category.name}</p>
                      <div
                        className="box_MdOutlineEdit"
                        onClick={() => {
                          togglePopupName(category.id);
                        }}
                      >
                        <MdOutlineEdit id="icon_edit_MdOutlineEdit" />
                      </div>
                    </div>
                  </div>
                ))
              : categories.map((category, index) => (
                  <div className="box_contact_category">
                    <div className="img">
                      <img src={category.image} alt="img" />
                    </div>
                    <div className="box_icon_MdOutlineEdit">
                      <p>{category.name}</p>
                    </div>
                  </div>
                ))}
            {}

            {isPopupImageCategory && (
              <form
                className="background_addproductpopup_box"
                onSubmit={ChangeCategoryImage}
              >
                <div className="hover_addproductpopup_box_image">
                  <div className="box_input_image">
                    <p>Edit Category image</p>
                    <label className="popup_Border_Boximagae">
                      {data ? (
                        <img src={URL.createObjectURL(data)} alt="category" />
                      ) : (
                        <img src={imageicon} alt="category" />
                      )}
                      <input
                        type="file"
                        id="img"
                        onChange={handleImageProductCategory}
                        required
                      />
                      <p className="box_choose_image">Choose img</p>
                    </label>
                  </div>
                  <div className="btn_foasdf">
                    <button
                      className="btn_cancel btn_addproducttxt_popup"
                      onClick={togglePopupCancelImageCategory}
                    >
                      Cancel
                    </button>
                    <button
                      className="btn_confirm btn_addproducttxt_popup"
                      type="submit"
                    >
                      Update
                    </button>
                  </div>
                </div>
              </form>
            )}
            {isPopupName && (
              <form
                className="background_addproductpopup_box"
                onSubmit={ChangeCategoryName}
              >
                <div className="hover_addproductpopup_box">
                  <div className="box_input">
                    <p>Edit category name</p>
                    <input
                      type="text"
                      placeholder="Name..."
                      className="input_of_txtAddproduct"
                      value={data}
                      onChange={(e) => {
                        set_data(e.target.value);
                      }}
                    />
                  </div>
                  <div className="btn_foasdf">
                    <button
                      className="btn_cancel btn_addproducttxt_popup"
                      onClick={togglePopupCancelName}
                    >
                      Cancel
                    </button>
                    <button
                      className="btn_confirm btn_addproducttxt_popup"
                      type="submit"
                    >
                      Update
                    </button>
                  </div>
                </div>
              </form>
            )}
          </div>

          <div id="container_product_admin">
            <div className="productHead_content">
              <h1 className="htxthead">
                <span className="spennofStyle"></span>ALL Product
              </h1>
            </div>
            <div className="contentImageProducts">
              {goods_list.map((product, index) => (
                <div className="box_product" key={index}>
                  <div className="box_input-img">
                    <div className="box_image">
                      <img src={`${import.meta.env.VITE_API}/${product.images}`} alt="Product" />
                      <input
                        type="file"
                        id={`image-${index}`}
                        onChange={(e) => handleImage(e, index)}
                        required
                      />
                    </div>

                    <div
                      className="Box_delete_product"
                      onClick={() => handleDelete(product.id)}
                    >
                      <AiOutlineDelete />
                    </div>

                    <div
                      className="edit_image_product"
                      onClick={() => openConfirmationPopupImage(product.id)}
                    >
                      <CiCamera id="box_icon_camera_product" />
                    </div>

                    {isConfirmationPopupOpenImage && (
                      <form
                        className="box_formUpdate"
                        onSubmit={ChangeProductImage}
                      >
                        <div className="formUpdate">
                          <div className="imageBox">
                            <p>Edit product image</p>
                            <label>
                              {data ? (
                                <img
                                  src={URL.createObjectURL(data)}
                                  alt="product"
                                />
                              ) : (
                                <img src={imageicon} alt="product" />
                              )}
                              <input
                                type="file"
                                id={`image-${index}`}
                                onChange={(e) => handleImage(e, index)}
                                required
                              />
                              <div className="choose">
                                <p>Choose img</p>
                              </div>
                            </label>
                          </div>
                          <div className="btn-update-del">
                            <button
                              className="btn_cancel btn_addproducttxt_popup"
                              onClick={closeConfirmationPopupImage}
                            >
                              Cancel
                            </button>
                            <button
                              className="btn_confirm btn_addproducttxt_popup"
                              type="submit"
                            >
                              Update
                            </button>
                          </div>
                        </div>
                      </form>
                    )}
                  </div>

                  <div className="txtOFproduct">
                    <div
                      className="box_icon_MdOutlineEdit"
                      onClick={() => openConfirmationPopup(product.id)}
                    >
                      <li>ProductName: {product.name}</li>
                      <MdOutlineEdit id="icon_edit" />
                    </div>
                    {isConfirmationPopupOpen && (
                      <div className="background_addproductpopup_box">
                        <div className="hover_addproductpopup_box">
                          <div className="box_input">
                            <p>Edit product name</p>
                            <input
                              type="text"
                              placeholder="Name..."
                              className="input_of_txtAddproduct"
                              value={data}
                              onChange={(e) => {
                                set_data(e.target.value);
                              }}
                            />
                          </div>
                          <div className="btn_foasdf">
                            <button
                              className="btn_cancel btn_addproducttxt_popup"
                              onClick={closeConfirmationPopup}
                            >
                              Cancel
                            </button>
                            <button
                              className="btn_confirm btn_addproducttxt_popup"
                              onClick={() => {
                                ChangeProductName();
                              }}
                            >
                              Update
                            </button>
                          </div>
                        </div>
                      </div>
                    )}

                    <div
                      className="box_icon_MdOutlineEdit"
                      onClick={() => openConfirmationPopupPrice(product.id)}
                    >
                      <li>Price: ${product.price}</li>
                      <MdOutlineEdit id="icon_edit" />
                    </div>
                    <div
                      className="box_icon_MdOutlineEdit"
                      onClick={() => openConfirmationPopupCategory(product.id)}
                    >
                      <li>Category: {product.category}</li>
                      <MdOutlineEdit id="icon_edit" />
                    </div>

                    {isConfirmationPopupOpenCategory && (
                      <div className="background_addproductpopup_box">
                        <div className="hover_addproductpopup_box">
                          <div className="box_input">
                            <p>Edit category</p>
                            <div className="box2">
                              <select
                                name="category"
                                className="product_category_filter"
                                required
                                onChange={(e) => set_data(e.target.value)}
                              >
                                <option className="inputproduct" value="">
                                  Select category
                                </option>
                                {categories.map((category) => (
                                  <option key={category.id} value={category.id}>
                                    {category.name}
                                  </option>
                                ))}
                              </select>
                            </div>
                          </div>
                          <div className="btn_foasdf">
                            <button
                              className="btn_cancel btn_addproducttxt_popup"
                              onClick={closeConfirmationPopupCategory}
                            >
                              Cancel
                            </button>
                            <button
                              className="btn_confirm btn_addproducttxt_popup"
                              onClick={() => {
                                ChangeProductCategory();
                              }}
                            >
                              Update
                            </button>
                          </div>
                        </div>
                      </div>
                    )}
                    {isConfirmationPopupOpenPrice && (
                      <div className="background_addproductpopup_box">
                        <div className="hover_addproductpopup_box">
                          <div className="box_input">
                            <p>Edit product price</p>
                            <input
                              type="text"
                              placeholder="Price..."
                              className="input_of_txtAddproduct"
                              value={data}
                              onChange={(e) => {
                                set_data(e.target.value);
                              }}
                            />
                          </div>
                          <div className="btn_foasdf">
                            <button
                              className="btn_cancel btn_addproducttxt_popup"
                              onClick={closeConfirmationPopupPrice}
                            >
                              Cancel
                            </button>
                            <button
                              className="btn_confirm btn_addproducttxt_popup"
                              onClick={() => {
                                ChangeProductPrice();
                              }}
                            >
                              Update
                            </button>
                          </div>
                        </div>
                      </div>
                    )}

                    <div
                      className="box_icon_MdOutlineEdit"
                      onClick={() => openConfirmationDesc(product.id)}
                    >
                      <li>Desc: {product.description}</li>
                      <MdOutlineEdit id="icon_edit" />
                    </div>
                    {isConfirmationDesc && (
                      <div className="background_addproductpopup_box">
                        <div className="hover_addproductpopup_box">
                          <div className="box_input">
                            <p>Edit Description</p>
                            <input
                              type="text"
                              placeholder="Description..."
                              className="input_of_txtAddproduct"
                              value={data}
                              onChange={(e) => {
                                set_data(e.target.value);
                              }}
                            />
                          </div>
                          <div className="btn_foasdf">
                            <button
                              className="btn_cancel btn_addproducttxt_popup"
                              onClick={closeConfirmationDesc}
                            >
                              Cancel
                            </button>
                            <button
                              className="btn_confirm btn_addproducttxt_popup"
                              onClick={() => {
                                ChangeProductDescription();
                              }}
                            >
                              Update
                            </button>
                          </div>
                        </div>
                      </div>
                    )}
                    <div
                      className="box_icon_MdOutlineEdit"
                      onClick={() =>
                        openConfirmationSize(product.id, product.sizes)
                      }
                    >
                      {/* <li>Size: {product.size}</li> */}
                      <li>
                        Size: {product.sizes.map((size) => size.name + " ")}
                      </li>
                      <MdOutlineEdit id="icon_edit" />
                    </div>
                    {isConfirmationSize && (
                      <div className="background_addproductpopup_box">
                        <div className="addproductpopup_box">
                          <div className="box_size_input">
                            <p>Edit product size</p>
                            <div className="box_size_container">
                              <div className="box_size_add">
                                {sizes.map((size, sizeIndex) => (
                                  <div
                                    key={sizeIndex}
                                    className="box_size_add_item"
                                  >
                                    <p>{size}</p>
                                    <span
                                      onClick={() => removeSizeInput(sizeIndex)}
                                    >
                                      <MdClose id="icon_MdClose" />
                                    </span>
                                  </div>
                                ))}
                              </div>

                              <div className="box_size_content">
                                <input
                                  type="text"
                                  placeholder="Add Sizes..."
                                  value={currentSize}
                                  onChange={(e) =>
                                    setCurrentSize(e.target.value)
                                  }
                                />
                                <div
                                  className="btn_addsize"
                                  onClick={() => addSizeInput()}
                                >
                                  Add
                                </div>
                              </div>
                            </div>
                          </div>
                          <div className="btn_foasdf">
                            <button
                              className="btn_cancel btn_addproducttxt_popup"
                              onClick={closeConfirmationSize}
                            >
                              Cancel
                            </button>
                            <button
                              className="btn_confirm btn_addproducttxt_popup"
                              onClick={() => {
                                ChangeProductSizes();
                              }}
                            >
                              Update
                            </button>
                          </div>
                        </div>
                      </div>
                    )}
                    <div
                      className="box_icon_MdOutlineEdit"
                      onClick={() =>
                        openConfirmationColor(product.id, product.colors)
                      }
                    >
                      <li>
                        Color: {product.colors.map((color) => color.name + " ")}
                      </li>
                      <MdOutlineEdit id="icon_edit" />
                    </div>
                    {isConfirmationColor && (
                      <div className="background_addproductpopup_box">
                        <div className="addproductpopup_box">
                          <div className="box_size_input">
                            <p>Edit product color</p>
                            <div className="box_size_container">
                              <div className="box_size_add">
                                {colors.map((color, colorIndex) => (
                                  <div
                                    key={colorIndex}
                                    className="box_size_add_item"
                                  >
                                    <p>{color}</p>
                                    <span
                                      onClick={() =>
                                        removeColorInput(colorIndex)
                                      }
                                    >
                                      <MdClose id="icon_MdClose" />
                                    </span>
                                  </div>
                                ))}
                              </div>

                              <div className="box_size_content">
                                <input
                                  type="text"
                                  placeholder="Add Colors..."
                                  value={currentColor}
                                  onChange={(e) =>
                                    setCurrentColor(e.target.value)
                                  }
                                />
                                <div
                                  className="btn_addsize"
                                  onClick={() => addColorInput()}
                                >
                                  Add
                                </div>
                              </div>
                            </div>
                          </div>
                          <div className="btn_foasdf">
                            <button
                              className="btn_cancel btn_addproducttxt_popup"
                              onClick={closeConfirmationColor}
                            >
                              Cancel
                            </button>
                            <button
                              className="btn_confirm btn_addproducttxt_popup"
                              onClick={() => {
                                ChangeProductColors();
                              }}
                            >
                              Update
                            </button>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default Product_Admin;
