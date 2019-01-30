import React from 'react';
import { Formik, Field, FieldArray } from 'formik';
import { connect } from 'react-redux';
import { updateUser, createUser } from '../redux/actions/users';


//need to grab a template from somewhere to drive the layout
const UserDetail = (props) => {
    var filteredFields = {fields:[]};
    var create = false;
    for(var i=0; i<props.fieldsToShow.length; i++)
    {
      var field = props.fieldsToShow[i];
      if (props.user) filteredFields['fields'].push({name: field, value: props.user.user[field], type: props.types[field]})
      else
      {
        filteredFields['fields'].push({name: field, value: "", type: props.types[field]})
        create = true;
      }
    }
    return ( 
      <div>
        <Formik
          initialValues={filteredFields}
          onSubmit={(values, actions) => {
            const user = Object.assign(props.user.user,values)
            if (create) {
              props.updateUser(props.user.index,user)
            }
            else {
              props.createUser(user)
            }
            setTimeout(() => {
              actions.setSubmitting(false);
            }, 1000);
          }}
          render={(props: FormikProps<Values>) => (
            <form onSubmit={props.handleSubmit}>
              <figure className="image is-4by3">
                  <img src={props.values['avatar']} alt="Large avatar Placeholder"></img>
              </figure>
              <FieldArray name="fields"
              render={ arrayHelpers => (
                <div>
                  props.values.fields.map((field, index) => (
                  <div key={index}>
                    return(<Field name={`fields[${index}].name`} value={field.value} static="is-static" component={CustomTextInputComponent}/>)
                  </div>
                  )

                })
                </div>
              )}
              />
              <button className="button" type="submit">{create?"Create":"Update"}</button>
            </form>
          )}
        />
      </div>
    )
};

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
