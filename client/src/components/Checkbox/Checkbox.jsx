import React from "react";

const CheckboxInput = ({
  checked,
  id,
  label,
  name,
  onChange,
  required,
}) => {
  const onInputValueChange = (event) => {
    const valueOverride = event.target.checked;

    onChange(event, valueOverride);
  };

  return (
    <section>
      <div className="checkbox pb-5">
        <label htmlFor={id} className="container">
          <input
            checked={checked}
            id={id}
            name={name}
            onChange={onInputValueChange}
            required={required}
            type="checkbox"
          />
          <span className="checkmark" />
          {label}
        </label>
      </div>
    </section>
  );
};

export default CheckboxInput;
