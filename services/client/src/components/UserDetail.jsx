import React from 'react';
import { Formik, Form, Field, FieldArray } from 'formik';
import { connect } from 'react-redux';
import { updateUser, createUser } from '../redux/actions/users';


//need to grab a template from somewhere to drive the layout
const UserDetail = (props) => {
    var filteredFields = {};
    var types = {};
    var create = false;
    for(var i=0; i<props.fieldsToShow.length; i++)
    {
      var field = props.fieldsToShow[i];
      if (props.user) 
      {
        filteredFields[field] = props.user.user[field]
      }
      else
      {
        filteredFields[field] = null
        create = true;
      }
    }
    filteredFields['types'] = props.types
    return ( 
      <div>
        <Formik
          initialValues={filteredFields}
          onSubmit={(values, actions) => {
            if (create) {
              console.log(values)
              props.createUser(values)
            }
            else {
              const user = Object.assign(props.user.user,values)
              props.updateUser(props.user.index,user)
            }
            setTimeout(() => {
              actions.setSubmitting(false);
            }, 1000);
          }}
          render={({ values }) => (
            <Form>
              <figure className="image is-4by3">
                  {console.log(values)}
                  <img src={values.avatar} alt="Large avatar Placeholder"></img>
              </figure>
                  {Object.keys(values).map((field, index) => {
                    switch(values.types[field]) {
                      case 'StringField' : 
                        return <div key={index}><Field name={field} static="is-static" component={CustomTextInputComponent}/></div>
                      case 'BooleanField' :
                        return <div key={index}><Field name={field} static="is-static" component={CustomCheckboxInputComponent}/></div>
                      default :
                        return null
                    }
                  })
                }
              <button className="button" type="submit">{create?"Create":"Update"}</button>
            </Form>
          )}
        />
      </div>
    )
}

const CustomTextInputComponent = ({
    field, // { name, value, onChange, onBlur }
    form: { touched, errors }, // also values, setXXXX, handleXXXX, dirty, isValid, status, etc.
    ...props
  }) => (
    <div className="field">
      <label className="label">{field.name}</label>
      <div className="control">
        <input className="input {props.static}" type="text" {...field} {...props} />
        {touched[field.name] &&
          errors[field.name] && <div className="error">{errors[field.name]}</div>}
      </div>
    </div>
  );

const CustomCheckboxInputComponent = ({
  field,
  form: { touched, errors },
  ...props
}) => (
  <div className="field">
    <label className="label">{field.name}</label>
      <input className="checkbox {props.static}" type="checkbox" {...field} {...props} />
      {touched[field.name] &&
        errors[field.name] && <div className="error">{errors[field.name]}</div>}
  </div>
);


const mapStateToProps = (state) => {
    return {
        types: state.userList.types,
        fieldsToShow: state.userList.fieldsToShow,
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
      updateUser: (index, user) => dispatch(updateUser(index, user)),
      createUser: (user) => dispatch(createUser(user))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(UserDetail);
