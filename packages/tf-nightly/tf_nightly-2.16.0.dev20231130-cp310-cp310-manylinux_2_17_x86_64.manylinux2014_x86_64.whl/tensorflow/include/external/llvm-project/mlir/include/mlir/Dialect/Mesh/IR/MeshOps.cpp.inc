/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Definitions                                                             *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|* From: MeshOps.td                                                           *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_OP_LIST
#undef GET_OP_LIST

::mlir::mesh::AllGatherOp,
::mlir::mesh::AllReduceOp,
::mlir::mesh::AllToAllOp,
::mlir::mesh::ClusterOp,
::mlir::mesh::ReduceScatterOp,
::mlir::mesh::ShardOp
#endif  // GET_OP_LIST

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace mesh {

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_MeshOps0(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((((::llvm::isa<::mlir::TensorType>(type))) && (((::llvm::cast<::mlir::ShapedType>(type).hasRank())) && ((::llvm::cast<::mlir::ShapedType>(type).getRank() >= 1)))) && ([](::mlir::Type elementType) { return (true); }(::llvm::cast<::mlir::ShapedType>(type).getElementType())))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be non-0-ranked.tensor of any type values, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_MeshOps1(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!(((::llvm::isa<::mlir::RankedTensorType>(type))) && ([](::mlir::Type elementType) { return (true); }(::llvm::cast<::mlir::ShapedType>(type).getElementType())))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be ranked tensor of any type values, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_MeshOps2(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((::llvm::isa<::mlir::RankedTensorType>(type)))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be Multi-dimensional array with a fixed number of dimensions, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps0(
    ::mlir::Attribute attr, ::llvm::StringRef attrName, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  if (attr && !((::llvm::isa<::mlir::FlatSymbolRefAttr>(attr))))
    return emitError() << "attribute '" << attrName
        << "' failed to satisfy constraint: flat symbol reference attribute";
  return ::mlir::success();
}
static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps0(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  return __mlir_ods_local_attr_constraint_MeshOps0(attr, attrName, [op]() {
    return op->emitOpError();
  });
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps1(
    ::mlir::Attribute attr, ::llvm::StringRef attrName, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  if (attr && !((::llvm::isa<::mlir::DenseI16ArrayAttr>(attr))))
    return emitError() << "attribute '" << attrName
        << "' failed to satisfy constraint: i16 dense array attribute";
  return ::mlir::success();
}
static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps1(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  return __mlir_ods_local_attr_constraint_MeshOps1(attr, attrName, [op]() {
    return op->emitOpError();
  });
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps2(
    ::mlir::Attribute attr, ::llvm::StringRef attrName, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  if (attr && !(((::llvm::isa<::mlir::IntegerAttr>(attr))) && ((::llvm::isa<::mlir::IndexType>(::llvm::cast<::mlir::IntegerAttr>(attr).getType())))))
    return emitError() << "attribute '" << attrName
        << "' failed to satisfy constraint: index attribute";
  return ::mlir::success();
}
static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps2(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  return __mlir_ods_local_attr_constraint_MeshOps2(attr, attrName, [op]() {
    return op->emitOpError();
  });
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps3(
    ::mlir::Attribute attr, ::llvm::StringRef attrName, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  if (attr && !((::llvm::isa<::mlir::mesh::PartialAttr>(attr))))
    return emitError() << "attribute '" << attrName
        << "' failed to satisfy constraint: partial type of a distributed tensor";
  return ::mlir::success();
}
static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps3(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  return __mlir_ods_local_attr_constraint_MeshOps3(attr, attrName, [op]() {
    return op->emitOpError();
  });
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps4(
    ::mlir::Attribute attr, ::llvm::StringRef attrName, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  if (attr && !((::llvm::isa<::mlir::StringAttr>(attr))))
    return emitError() << "attribute '" << attrName
        << "' failed to satisfy constraint: string attribute";
  return ::mlir::success();
}
static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps4(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  return __mlir_ods_local_attr_constraint_MeshOps4(attr, attrName, [op]() {
    return op->emitOpError();
  });
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps5(
    ::mlir::Attribute attr, ::llvm::StringRef attrName, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  if (attr && !(((::llvm::isa<::mlir::IntegerAttr>(attr))) && ((::llvm::cast<::mlir::IntegerAttr>(attr).getType().isSignlessInteger(64)))))
    return emitError() << "attribute '" << attrName
        << "' failed to satisfy constraint: 64-bit signless integer attribute";
  return ::mlir::success();
}
static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps5(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  return __mlir_ods_local_attr_constraint_MeshOps5(attr, attrName, [op]() {
    return op->emitOpError();
  });
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps6(
    ::mlir::Attribute attr, ::llvm::StringRef attrName, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  if (attr && !((::llvm::isa<::mlir::DenseI64ArrayAttr>(attr))))
    return emitError() << "attribute '" << attrName
        << "' failed to satisfy constraint: i64 dense array attribute";
  return ::mlir::success();
}
static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps6(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  return __mlir_ods_local_attr_constraint_MeshOps6(attr, attrName, [op]() {
    return op->emitOpError();
  });
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps7(
    ::mlir::Attribute attr, ::llvm::StringRef attrName, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  if (attr && !((::llvm::isa<::mlir::mesh::MeshShardingAttr>(attr))))
    return emitError() << "attribute '" << attrName
        << "' failed to satisfy constraint: Attribute that extends tensor type to distributed tensor type.";
  return ::mlir::success();
}
static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps7(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  return __mlir_ods_local_attr_constraint_MeshOps7(attr, attrName, [op]() {
    return op->emitOpError();
  });
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps8(
    ::mlir::Attribute attr, ::llvm::StringRef attrName, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  if (attr && !((::llvm::isa<::mlir::UnitAttr>(attr))))
    return emitError() << "attribute '" << attrName
        << "' failed to satisfy constraint: unit attribute";
  return ::mlir::success();
}
static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_MeshOps8(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  return __mlir_ods_local_attr_constraint_MeshOps8(attr, attrName, [op]() {
    return op->emitOpError();
  });
}
} // namespace mesh
} // namespace mlir
namespace mlir {
namespace mesh {

//===----------------------------------------------------------------------===//
// ::mlir::mesh::AllGatherOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
AllGatherOpGenericAdaptorBase::AllGatherOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, const Properties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), properties(properties), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("mesh.all_gather", odsAttrs.getContext());
}

AllGatherOpGenericAdaptorBase::AllGatherOpGenericAdaptorBase(AllGatherOp op) : AllGatherOpGenericAdaptorBase(op->getDiscardableAttrDictionary(), op.getProperties(), op->getRegions()) {}

std::pair<unsigned, unsigned> AllGatherOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr AllGatherOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

::mlir::FlatSymbolRefAttr AllGatherOpGenericAdaptorBase::getMeshAttr() {
  auto attr = ::llvm::cast<::mlir::FlatSymbolRefAttr>(getProperties().mesh);
  return attr;
}

::llvm::StringRef AllGatherOpGenericAdaptorBase::getMesh() {
  auto attr = getMeshAttr();
  return attr.getValue();
}

::mlir::DenseI16ArrayAttr AllGatherOpGenericAdaptorBase::getMeshAxesAttr() {
  auto attr = ::llvm::dyn_cast_or_null<::mlir::DenseI16ArrayAttr>(getProperties().mesh_axes);
  return attr;
}

::llvm::ArrayRef<int16_t> AllGatherOpGenericAdaptorBase::getMeshAxes() {
  auto attr = getMeshAxesAttr();
  return attr;
}

::mlir::IntegerAttr AllGatherOpGenericAdaptorBase::getGatherAxisAttr() {
  auto attr = ::llvm::cast<::mlir::IntegerAttr>(getProperties().gather_axis);
  return attr;
}

::llvm::APInt AllGatherOpGenericAdaptorBase::getGatherAxis() {
  auto attr = getGatherAxisAttr();
  return attr.getValue();
}

} // namespace detail
AllGatherOpAdaptor::AllGatherOpAdaptor(AllGatherOp op) : AllGatherOpGenericAdaptor(op->getOperands(), op) {}

::mlir::LogicalResult AllGatherOpAdaptor::verify(::mlir::Location loc) {
  auto tblgen_gather_axis = getProperties().gather_axis; (void)tblgen_gather_axis;
  if (!tblgen_gather_axis) return emitError(loc, "'mesh.all_gather' op ""requires attribute 'gather_axis'");
  auto tblgen_mesh = getProperties().mesh; (void)tblgen_mesh;
  if (!tblgen_mesh) return emitError(loc, "'mesh.all_gather' op ""requires attribute 'mesh'");
  auto tblgen_mesh_axes = getProperties().mesh_axes; (void)tblgen_mesh_axes;

  if (tblgen_mesh && !((::llvm::isa<::mlir::FlatSymbolRefAttr>(tblgen_mesh))))
    return emitError(loc, "'mesh.all_gather' op ""attribute 'mesh' failed to satisfy constraint: flat symbol reference attribute");

  if (tblgen_mesh_axes && !((::llvm::isa<::mlir::DenseI16ArrayAttr>(tblgen_mesh_axes))))
    return emitError(loc, "'mesh.all_gather' op ""attribute 'mesh_axes' failed to satisfy constraint: i16 dense array attribute");

  if (tblgen_gather_axis && !(((::llvm::isa<::mlir::IntegerAttr>(tblgen_gather_axis))) && ((::llvm::isa<::mlir::IndexType>(::llvm::cast<::mlir::IntegerAttr>(tblgen_gather_axis).getType())))))
    return emitError(loc, "'mesh.all_gather' op ""attribute 'gather_axis' failed to satisfy constraint: index attribute");
  return ::mlir::success();
}

std::pair<unsigned, unsigned> AllGatherOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range AllGatherOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::TypedValue<::mlir::TensorType> AllGatherOp::getInput() {
  return ::llvm::cast<::mlir::TypedValue<::mlir::TensorType>>(*getODSOperands(0).begin());
}

::mlir::OpOperand &AllGatherOp::getInputMutable() {
  auto range = getODSOperandIndexAndLength(0);
  return getOperation()->getOpOperand(range.first);
}

std::pair<unsigned, unsigned> AllGatherOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range AllGatherOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::TypedValue<::mlir::TensorType> AllGatherOp::getResult() {
  return ::llvm::cast<::mlir::TypedValue<::mlir::TensorType>>(*getODSResults(0).begin());
}

::mlir::LogicalResult AllGatherOp::setPropertiesFromAttr(Properties &prop, ::mlir::Attribute attr, ::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  ::mlir::DictionaryAttr dict = ::llvm::dyn_cast<::mlir::DictionaryAttr>(attr);
  if (!dict) {
    emitError() << "expected DictionaryAttr to set properties";
    return ::mlir::failure();
  }

  {
    auto &propStorage = prop.gather_axis;
       auto attr = dict.get("gather_axis");
    if (attr || /*isRequired=*/true) {
      if (!attr) {
        emitError() << "expected key entry for gather_axis in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `gather_axis` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }

  {
    auto &propStorage = prop.mesh;
       auto attr = dict.get("mesh");
    if (attr || /*isRequired=*/true) {
      if (!attr) {
        emitError() << "expected key entry for mesh in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `mesh` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }

  {
    auto &propStorage = prop.mesh_axes;
       auto attr = dict.get("mesh_axes");
    if (attr || /*isRequired=*/false) {
      if (!attr) {
        emitError() << "expected key entry for mesh_axes in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `mesh_axes` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }
  return ::mlir::success();
}

::mlir::Attribute AllGatherOp::getPropertiesAsAttr(::mlir::MLIRContext *ctx, const Properties &prop) {
    ::mlir::SmallVector<::mlir::NamedAttribute> attrs;
    ::mlir::Builder odsBuilder{ctx};

    {
      const auto &propStorage = prop.gather_axis;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("gather_axis",
                                       propStorage));
    }

    {
      const auto &propStorage = prop.mesh;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("mesh",
                                       propStorage));
    }

    {
      const auto &propStorage = prop.mesh_axes;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("mesh_axes",
                                       propStorage));
    }

  if (!attrs.empty())
    return odsBuilder.getDictionaryAttr(attrs);
  return {};
}

llvm::hash_code AllGatherOp::computePropertiesHash(const Properties &prop) {
  return llvm::hash_combine(
    llvm::hash_value(prop.gather_axis.getAsOpaquePointer()), 
    llvm::hash_value(prop.mesh.getAsOpaquePointer()), 
    llvm::hash_value(prop.mesh_axes.getAsOpaquePointer()));
}

std::optional<mlir::Attribute> AllGatherOp::getInherentAttr(::mlir::MLIRContext *ctx, const Properties &prop, llvm::StringRef name) {
    if (name == "gather_axis")
      return prop.gather_axis;

    if (name == "mesh")
      return prop.mesh;

    if (name == "mesh_axes")
      return prop.mesh_axes;
  return std::nullopt;
}

void AllGatherOp::setInherentAttr(Properties &prop, llvm::StringRef name, mlir::Attribute value) {
    if (name == "gather_axis") {
       prop.gather_axis = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.gather_axis)>>(value);
       return;
    }

    if (name == "mesh") {
       prop.mesh = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.mesh)>>(value);
       return;
    }

    if (name == "mesh_axes") {
       prop.mesh_axes = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.mesh_axes)>>(value);
       return;
    }
}

void AllGatherOp::populateInherentAttrs(::mlir::MLIRContext *ctx, const Properties &prop, ::mlir::NamedAttrList &attrs) {
    if (prop.gather_axis) attrs.append("gather_axis", prop.gather_axis);

    if (prop.mesh) attrs.append("mesh", prop.mesh);

    if (prop.mesh_axes) attrs.append("mesh_axes", prop.mesh_axes);
}

::mlir::LogicalResult AllGatherOp::verifyInherentAttrs(::mlir::OperationName opName, ::mlir::NamedAttrList &attrs, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
    {
      ::mlir::Attribute attr = attrs.get(getGatherAxisAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps2(attr, "gather_axis", emitError)))
        return ::mlir::failure();
    }

    {
      ::mlir::Attribute attr = attrs.get(getMeshAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps0(attr, "mesh", emitError)))
        return ::mlir::failure();
    }

    {
      ::mlir::Attribute attr = attrs.get(getMeshAxesAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps1(attr, "mesh_axes", emitError)))
        return ::mlir::failure();
    }
    return ::mlir::success();
}

::mlir::LogicalResult AllGatherOp::readProperties(::mlir::DialectBytecodeReader &reader, ::mlir::OperationState &state) {
  auto &prop = state.getOrAddProperties<Properties>(); (void)prop;
  if (::mlir::failed(reader.readAttribute(prop.gather_axis)))
    return ::mlir::failure();

  if (::mlir::failed(reader.readAttribute(prop.mesh)))
    return ::mlir::failure();

  if (::mlir::failed(reader.readOptionalAttribute(prop.mesh_axes)))
    return ::mlir::failure();
  return ::mlir::success();
}

void AllGatherOp::writeProperties(::mlir::DialectBytecodeWriter &writer) {
  auto &prop = getProperties(); (void)prop;
  writer.writeAttribute(prop.gather_axis);
  writer.writeAttribute(prop.mesh);

  writer.writeOptionalAttribute(prop.mesh_axes);
}

::mlir::FlatSymbolRefAttr AllGatherOp::getMeshAttr() {
  return ::llvm::cast<::mlir::FlatSymbolRefAttr>(getProperties().mesh);
}

::llvm::StringRef AllGatherOp::getMesh() {
  auto attr = getMeshAttr();
  return attr.getValue();
}

::mlir::DenseI16ArrayAttr AllGatherOp::getMeshAxesAttr() {
  return ::llvm::dyn_cast_or_null<::mlir::DenseI16ArrayAttr>(getProperties().mesh_axes);
}

::llvm::ArrayRef<int16_t> AllGatherOp::getMeshAxes() {
  auto attr = getMeshAxesAttr();
  return attr;
}

::mlir::IntegerAttr AllGatherOp::getGatherAxisAttr() {
  return ::llvm::cast<::mlir::IntegerAttr>(getProperties().gather_axis);
}

::llvm::APInt AllGatherOp::getGatherAxis() {
  auto attr = getGatherAxisAttr();
  return attr.getValue();
}

void AllGatherOp::setMeshAttr(::mlir::FlatSymbolRefAttr attr) {
  (*this)->setAttr(getMeshAttrName(), attr);
}

void AllGatherOp::setMesh(::llvm::StringRef attrValue) {
  (*this)->setAttr(getMeshAttrName(), ::mlir::SymbolRefAttr::get(::mlir::Builder((*this)->getContext()).getContext(), attrValue));
}

void AllGatherOp::setMeshAxesAttr(::mlir::DenseI16ArrayAttr attr) {
  (*this)->setAttr(getMeshAxesAttrName(), attr);
}

void AllGatherOp::setMeshAxes(::llvm::ArrayRef<int16_t> attrValue) {
  (*this)->setAttr(getMeshAxesAttrName(), ::mlir::Builder((*this)->getContext()).getDenseI16ArrayAttr(attrValue));
}

void AllGatherOp::setGatherAxisAttr(::mlir::IntegerAttr attr) {
  (*this)->setAttr(getGatherAxisAttrName(), attr);
}

void AllGatherOp::setGatherAxis(::llvm::APInt attrValue) {
  (*this)->setAttr(getGatherAxisAttrName(), ::mlir::Builder((*this)->getContext()).getIntegerAttr(::mlir::Builder((*this)->getContext()).getIndexType(), attrValue));
}

void AllGatherOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::IntegerAttr gather_axis) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = mesh;
  if (mesh_axes) {
    odsState.getOrAddProperties<Properties>().mesh_axes = mesh_axes;
  }
  odsState.getOrAddProperties<Properties>().gather_axis = gather_axis;
  odsState.addTypes(result);
}

void AllGatherOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::IntegerAttr gather_axis) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = mesh;
  if (mesh_axes) {
    odsState.getOrAddProperties<Properties>().mesh_axes = mesh_axes;
  }
  odsState.getOrAddProperties<Properties>().gather_axis = gather_axis;
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void AllGatherOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::llvm::APInt gather_axis) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = ::mlir::SymbolRefAttr::get(odsBuilder.getContext(), mesh);
  odsState.getOrAddProperties<Properties>().mesh_axes = odsBuilder.getDenseI16ArrayAttr(mesh_axes);
  odsState.getOrAddProperties<Properties>().gather_axis = odsBuilder.getIntegerAttr(odsBuilder.getIndexType(), gather_axis);
  odsState.addTypes(result);
}

void AllGatherOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::llvm::APInt gather_axis) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = ::mlir::SymbolRefAttr::get(odsBuilder.getContext(), mesh);
  odsState.getOrAddProperties<Properties>().mesh_axes = odsBuilder.getDenseI16ArrayAttr(mesh_axes);
  odsState.getOrAddProperties<Properties>().gather_axis = odsBuilder.getIntegerAttr(odsBuilder.getIndexType(), gather_axis);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void AllGatherOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

void AllGatherOp::populateDefaultProperties(::mlir::OperationName opName, Properties &properties) {
  ::mlir::Builder odsBuilder(opName.getContext());
  if (!properties.mesh_axes)
    properties.mesh_axes = odsBuilder.getDenseI16ArrayAttr({});
}

::mlir::LogicalResult AllGatherOp::verifyInvariantsImpl() {
  auto tblgen_gather_axis = getProperties().gather_axis; (void)tblgen_gather_axis;
  if (!tblgen_gather_axis) return emitOpError("requires attribute 'gather_axis'");
  auto tblgen_mesh = getProperties().mesh; (void)tblgen_mesh;
  if (!tblgen_mesh) return emitOpError("requires attribute 'mesh'");
  auto tblgen_mesh_axes = getProperties().mesh_axes; (void)tblgen_mesh_axes;

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps0(*this, tblgen_mesh, "mesh")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps1(*this, tblgen_mesh_axes, "mesh_axes")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps2(*this, tblgen_gather_axis, "gather_axis")))
    return ::mlir::failure();
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_MeshOps0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_MeshOps0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult AllGatherOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

::mlir::ParseResult AllGatherOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::UnresolvedOperand inputRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::UnresolvedOperand> inputOperands(inputRawOperands);  ::llvm::SMLoc inputOperandsLoc;
  (void)inputOperandsLoc;
  ::mlir::FlatSymbolRefAttr meshAttr;
  ::mlir::DenseI16ArrayAttr mesh_axesAttr;
  ::mlir::IntegerAttr gather_axisAttr;
  ::mlir::Type inputRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> inputTypes(inputRawTypes);
  ::mlir::Type resultRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> resultTypes(resultRawTypes);

  inputOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(inputRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseKeyword("on"))
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(meshAttr, parser.getBuilder().getType<::mlir::NoneType>())) {
    return ::mlir::failure();
  }
  if (meshAttr) result.getOrAddProperties<AllGatherOp::Properties>().mesh = meshAttr;
  if (::mlir::succeeded(parser.parseOptionalKeyword("mesh_axes"))) {
  if (parser.parseEqual())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(mesh_axesAttr, ::mlir::Type{})) {
    return ::mlir::failure();
  }
  if (mesh_axesAttr) result.getOrAddProperties<AllGatherOp::Properties>().mesh_axes = mesh_axesAttr;
  }
  if (parser.parseKeyword("gather_axis"))
    return ::mlir::failure();
  if (parser.parseEqual())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(gather_axisAttr, parser.getBuilder().getIndexType())) {
    return ::mlir::failure();
  }
  if (gather_axisAttr) result.getOrAddProperties<AllGatherOp::Properties>().gather_axis = gather_axisAttr;
  {
    auto loc = parser.getCurrentLocation();(void)loc;
    if (parser.parseOptionalAttrDict(result.attributes))
      return ::mlir::failure();
    if (failed(verifyInherentAttrs(result.name, result.attributes, [&]() {
        return parser.emitError(loc) << "'" << result.name.getStringRef() << "' op ";
      })))
      return ::mlir::failure();
  }
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::TensorType type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    inputRawTypes[0] = type;
  }
  if (parser.parseArrow())
    return ::mlir::failure();

  {
    ::mlir::TensorType type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    resultRawTypes[0] = type;
  }
  result.addTypes(resultTypes);
  if (parser.resolveOperands(inputOperands, inputTypes, inputOperandsLoc, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void AllGatherOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  _odsPrinter << getInput();
  _odsPrinter << ' ' << "on";
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(getMeshAttr());
  if (getMeshAxesAttr() && getMeshAxesAttr() != ::mlir::OpBuilder((*this)->getContext()).getDenseI16ArrayAttr({})) {
    _odsPrinter << ' ' << "mesh_axes";
    _odsPrinter << ' ' << "=";
    _odsPrinter << ' ';
  _odsPrinter.printStrippedAttrOrType(getMeshAxesAttr());
  }
  _odsPrinter << ' ' << "gather_axis";
  _odsPrinter << ' ' << "=";
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(getGatherAxisAttr());
  ::llvm::SmallVector<::llvm::StringRef, 2> elidedAttrs;
  elidedAttrs.push_back("mesh");
  elidedAttrs.push_back("mesh_axes");
  elidedAttrs.push_back("gather_axis");
  {
     ::mlir::Builder odsBuilder(getContext());
     ::mlir::Attribute attr = getMeshAxesAttr();
     if(attr && (attr == odsBuilder.getDenseI16ArrayAttr({})))
       elidedAttrs.push_back("mesh_axes");
  }
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), elidedAttrs);
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = getInput().getType();
    if (auto validType = ::llvm::dyn_cast<::mlir::TensorType>(type))
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
  _odsPrinter << ' ' << "->";
  _odsPrinter << ' ';
  {
    auto type = getResult().getType();
    if (auto validType = ::llvm::dyn_cast<::mlir::TensorType>(type))
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

} // namespace mesh
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::mesh::AllGatherOp)

namespace mlir {
namespace mesh {

//===----------------------------------------------------------------------===//
// ::mlir::mesh::AllReduceOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
AllReduceOpGenericAdaptorBase::AllReduceOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, const Properties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), properties(properties), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("mesh.all_reduce", odsAttrs.getContext());
}

AllReduceOpGenericAdaptorBase::AllReduceOpGenericAdaptorBase(AllReduceOp op) : AllReduceOpGenericAdaptorBase(op->getDiscardableAttrDictionary(), op.getProperties(), op->getRegions()) {}

std::pair<unsigned, unsigned> AllReduceOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr AllReduceOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

::mlir::FlatSymbolRefAttr AllReduceOpGenericAdaptorBase::getMeshAttr() {
  auto attr = ::llvm::cast<::mlir::FlatSymbolRefAttr>(getProperties().mesh);
  return attr;
}

::llvm::StringRef AllReduceOpGenericAdaptorBase::getMesh() {
  auto attr = getMeshAttr();
  return attr.getValue();
}

::mlir::DenseI16ArrayAttr AllReduceOpGenericAdaptorBase::getMeshAxesAttr() {
  auto attr = ::llvm::dyn_cast_or_null<::mlir::DenseI16ArrayAttr>(getProperties().mesh_axes);
  return attr;
}

::llvm::ArrayRef<int16_t> AllReduceOpGenericAdaptorBase::getMeshAxes() {
  auto attr = getMeshAxesAttr();
  return attr;
}

::mlir::mesh::PartialAttr AllReduceOpGenericAdaptorBase::getReductionAttr() {
  auto attr = ::llvm::dyn_cast_or_null<::mlir::mesh::PartialAttr>(getProperties().reduction);
  return attr;
}

::mlir::mesh::Partial AllReduceOpGenericAdaptorBase::getReduction() {
  auto attr = getReductionAttr();
  return attr.getValue();
}

} // namespace detail
AllReduceOpAdaptor::AllReduceOpAdaptor(AllReduceOp op) : AllReduceOpGenericAdaptor(op->getOperands(), op) {}

::mlir::LogicalResult AllReduceOpAdaptor::verify(::mlir::Location loc) {
  auto tblgen_mesh = getProperties().mesh; (void)tblgen_mesh;
  if (!tblgen_mesh) return emitError(loc, "'mesh.all_reduce' op ""requires attribute 'mesh'");
  auto tblgen_mesh_axes = getProperties().mesh_axes; (void)tblgen_mesh_axes;
  auto tblgen_reduction = getProperties().reduction; (void)tblgen_reduction;

  if (tblgen_mesh && !((::llvm::isa<::mlir::FlatSymbolRefAttr>(tblgen_mesh))))
    return emitError(loc, "'mesh.all_reduce' op ""attribute 'mesh' failed to satisfy constraint: flat symbol reference attribute");

  if (tblgen_mesh_axes && !((::llvm::isa<::mlir::DenseI16ArrayAttr>(tblgen_mesh_axes))))
    return emitError(loc, "'mesh.all_reduce' op ""attribute 'mesh_axes' failed to satisfy constraint: i16 dense array attribute");

  if (tblgen_reduction && !((::llvm::isa<::mlir::mesh::PartialAttr>(tblgen_reduction))))
    return emitError(loc, "'mesh.all_reduce' op ""attribute 'reduction' failed to satisfy constraint: partial type of a distributed tensor");
  return ::mlir::success();
}

std::pair<unsigned, unsigned> AllReduceOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range AllReduceOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::TypedValue<::mlir::RankedTensorType> AllReduceOp::getInput() {
  return ::llvm::cast<::mlir::TypedValue<::mlir::RankedTensorType>>(*getODSOperands(0).begin());
}

::mlir::OpOperand &AllReduceOp::getInputMutable() {
  auto range = getODSOperandIndexAndLength(0);
  return getOperation()->getOpOperand(range.first);
}

std::pair<unsigned, unsigned> AllReduceOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range AllReduceOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::TypedValue<::mlir::RankedTensorType> AllReduceOp::getResult() {
  return ::llvm::cast<::mlir::TypedValue<::mlir::RankedTensorType>>(*getODSResults(0).begin());
}

::mlir::LogicalResult AllReduceOp::setPropertiesFromAttr(Properties &prop, ::mlir::Attribute attr, ::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  ::mlir::DictionaryAttr dict = ::llvm::dyn_cast<::mlir::DictionaryAttr>(attr);
  if (!dict) {
    emitError() << "expected DictionaryAttr to set properties";
    return ::mlir::failure();
  }

  {
    auto &propStorage = prop.mesh;
       auto attr = dict.get("mesh");
    if (attr || /*isRequired=*/true) {
      if (!attr) {
        emitError() << "expected key entry for mesh in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `mesh` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }

  {
    auto &propStorage = prop.mesh_axes;
       auto attr = dict.get("mesh_axes");
    if (attr || /*isRequired=*/false) {
      if (!attr) {
        emitError() << "expected key entry for mesh_axes in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `mesh_axes` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }

  {
    auto &propStorage = prop.reduction;
       auto attr = dict.get("reduction");
    if (attr || /*isRequired=*/false) {
      if (!attr) {
        emitError() << "expected key entry for reduction in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `reduction` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }
  return ::mlir::success();
}

::mlir::Attribute AllReduceOp::getPropertiesAsAttr(::mlir::MLIRContext *ctx, const Properties &prop) {
    ::mlir::SmallVector<::mlir::NamedAttribute> attrs;
    ::mlir::Builder odsBuilder{ctx};

    {
      const auto &propStorage = prop.mesh;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("mesh",
                                       propStorage));
    }

    {
      const auto &propStorage = prop.mesh_axes;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("mesh_axes",
                                       propStorage));
    }

    {
      const auto &propStorage = prop.reduction;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("reduction",
                                       propStorage));
    }

  if (!attrs.empty())
    return odsBuilder.getDictionaryAttr(attrs);
  return {};
}

llvm::hash_code AllReduceOp::computePropertiesHash(const Properties &prop) {
  return llvm::hash_combine(
    llvm::hash_value(prop.mesh.getAsOpaquePointer()), 
    llvm::hash_value(prop.mesh_axes.getAsOpaquePointer()), 
    llvm::hash_value(prop.reduction.getAsOpaquePointer()));
}

std::optional<mlir::Attribute> AllReduceOp::getInherentAttr(::mlir::MLIRContext *ctx, const Properties &prop, llvm::StringRef name) {
    if (name == "mesh")
      return prop.mesh;

    if (name == "mesh_axes")
      return prop.mesh_axes;

    if (name == "reduction")
      return prop.reduction;
  return std::nullopt;
}

void AllReduceOp::setInherentAttr(Properties &prop, llvm::StringRef name, mlir::Attribute value) {
    if (name == "mesh") {
       prop.mesh = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.mesh)>>(value);
       return;
    }

    if (name == "mesh_axes") {
       prop.mesh_axes = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.mesh_axes)>>(value);
       return;
    }

    if (name == "reduction") {
       prop.reduction = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.reduction)>>(value);
       return;
    }
}

void AllReduceOp::populateInherentAttrs(::mlir::MLIRContext *ctx, const Properties &prop, ::mlir::NamedAttrList &attrs) {
    if (prop.mesh) attrs.append("mesh", prop.mesh);

    if (prop.mesh_axes) attrs.append("mesh_axes", prop.mesh_axes);

    if (prop.reduction) attrs.append("reduction", prop.reduction);
}

::mlir::LogicalResult AllReduceOp::verifyInherentAttrs(::mlir::OperationName opName, ::mlir::NamedAttrList &attrs, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
    {
      ::mlir::Attribute attr = attrs.get(getMeshAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps0(attr, "mesh", emitError)))
        return ::mlir::failure();
    }

    {
      ::mlir::Attribute attr = attrs.get(getMeshAxesAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps1(attr, "mesh_axes", emitError)))
        return ::mlir::failure();
    }

    {
      ::mlir::Attribute attr = attrs.get(getReductionAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps3(attr, "reduction", emitError)))
        return ::mlir::failure();
    }
    return ::mlir::success();
}

::mlir::LogicalResult AllReduceOp::readProperties(::mlir::DialectBytecodeReader &reader, ::mlir::OperationState &state) {
  auto &prop = state.getOrAddProperties<Properties>(); (void)prop;
  if (::mlir::failed(reader.readAttribute(prop.mesh)))
    return ::mlir::failure();

  if (::mlir::failed(reader.readOptionalAttribute(prop.mesh_axes)))
    return ::mlir::failure();

  if (::mlir::failed(reader.readOptionalAttribute(prop.reduction)))
    return ::mlir::failure();
  return ::mlir::success();
}

void AllReduceOp::writeProperties(::mlir::DialectBytecodeWriter &writer) {
  auto &prop = getProperties(); (void)prop;
  writer.writeAttribute(prop.mesh);

  writer.writeOptionalAttribute(prop.mesh_axes);

  writer.writeOptionalAttribute(prop.reduction);
}

::mlir::FlatSymbolRefAttr AllReduceOp::getMeshAttr() {
  return ::llvm::cast<::mlir::FlatSymbolRefAttr>(getProperties().mesh);
}

::llvm::StringRef AllReduceOp::getMesh() {
  auto attr = getMeshAttr();
  return attr.getValue();
}

::mlir::DenseI16ArrayAttr AllReduceOp::getMeshAxesAttr() {
  return ::llvm::dyn_cast_or_null<::mlir::DenseI16ArrayAttr>(getProperties().mesh_axes);
}

::llvm::ArrayRef<int16_t> AllReduceOp::getMeshAxes() {
  auto attr = getMeshAxesAttr();
  return attr;
}

::mlir::mesh::PartialAttr AllReduceOp::getReductionAttr() {
  return ::llvm::dyn_cast_or_null<::mlir::mesh::PartialAttr>(getProperties().reduction);
}

::mlir::mesh::Partial AllReduceOp::getReduction() {
  auto attr = getReductionAttr();
  return attr.getValue();
}

void AllReduceOp::setMeshAttr(::mlir::FlatSymbolRefAttr attr) {
  (*this)->setAttr(getMeshAttrName(), attr);
}

void AllReduceOp::setMesh(::llvm::StringRef attrValue) {
  (*this)->setAttr(getMeshAttrName(), ::mlir::SymbolRefAttr::get(::mlir::Builder((*this)->getContext()).getContext(), attrValue));
}

void AllReduceOp::setMeshAxesAttr(::mlir::DenseI16ArrayAttr attr) {
  (*this)->setAttr(getMeshAxesAttrName(), attr);
}

void AllReduceOp::setMeshAxes(::llvm::ArrayRef<int16_t> attrValue) {
  (*this)->setAttr(getMeshAxesAttrName(), ::mlir::Builder((*this)->getContext()).getDenseI16ArrayAttr(attrValue));
}

void AllReduceOp::setReductionAttr(::mlir::mesh::PartialAttr attr) {
  (*this)->setAttr(getReductionAttrName(), attr);
}

void AllReduceOp::setReduction(::mlir::mesh::Partial attrValue) {
  (*this)->setAttr(getReductionAttrName(), ::mlir::mesh::PartialAttr::get(::mlir::Builder((*this)->getContext()).getContext(), attrValue));
}

void AllReduceOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::mesh::PartialAttr reduction) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = mesh;
  if (mesh_axes) {
    odsState.getOrAddProperties<Properties>().mesh_axes = mesh_axes;
  }
  if (reduction) {
    odsState.getOrAddProperties<Properties>().reduction = reduction;
  }
  odsState.addTypes(result);
}

void AllReduceOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::mesh::PartialAttr reduction) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = mesh;
  if (mesh_axes) {
    odsState.getOrAddProperties<Properties>().mesh_axes = mesh_axes;
  }
  if (reduction) {
    odsState.getOrAddProperties<Properties>().reduction = reduction;
  }
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void AllReduceOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::mlir::mesh::Partial reduction) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = ::mlir::SymbolRefAttr::get(odsBuilder.getContext(), mesh);
  odsState.getOrAddProperties<Properties>().mesh_axes = odsBuilder.getDenseI16ArrayAttr(mesh_axes);
  odsState.getOrAddProperties<Properties>().reduction = ::mlir::mesh::PartialAttr::get(odsBuilder.getContext(), reduction);
  odsState.addTypes(result);
}

void AllReduceOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::mlir::mesh::Partial reduction) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = ::mlir::SymbolRefAttr::get(odsBuilder.getContext(), mesh);
  odsState.getOrAddProperties<Properties>().mesh_axes = odsBuilder.getDenseI16ArrayAttr(mesh_axes);
  odsState.getOrAddProperties<Properties>().reduction = ::mlir::mesh::PartialAttr::get(odsBuilder.getContext(), reduction);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void AllReduceOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

void AllReduceOp::populateDefaultProperties(::mlir::OperationName opName, Properties &properties) {
  ::mlir::Builder odsBuilder(opName.getContext());
  if (!properties.mesh_axes)
    properties.mesh_axes = odsBuilder.getDenseI16ArrayAttr({});
  if (!properties.reduction)
    properties.reduction = ::mlir::mesh::PartialAttr::get(odsBuilder.getContext(), ::mlir::mesh::Partial::Sum);
}

::mlir::LogicalResult AllReduceOp::verifyInvariantsImpl() {
  auto tblgen_mesh = getProperties().mesh; (void)tblgen_mesh;
  if (!tblgen_mesh) return emitOpError("requires attribute 'mesh'");
  auto tblgen_mesh_axes = getProperties().mesh_axes; (void)tblgen_mesh_axes;
  auto tblgen_reduction = getProperties().reduction; (void)tblgen_reduction;

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps0(*this, tblgen_mesh, "mesh")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps1(*this, tblgen_mesh_axes, "mesh_axes")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps3(*this, tblgen_reduction, "reduction")))
    return ::mlir::failure();
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_MeshOps1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_MeshOps1(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult AllReduceOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

::mlir::ParseResult AllReduceOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::UnresolvedOperand inputRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::UnresolvedOperand> inputOperands(inputRawOperands);  ::llvm::SMLoc inputOperandsLoc;
  (void)inputOperandsLoc;
  ::mlir::FlatSymbolRefAttr meshAttr;
  ::mlir::DenseI16ArrayAttr mesh_axesAttr;
  ::mlir::mesh::PartialAttr reductionAttr;
  ::mlir::Type inputRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> inputTypes(inputRawTypes);
  ::mlir::Type resultRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> resultTypes(resultRawTypes);

  inputOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(inputRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseKeyword("on"))
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(meshAttr, parser.getBuilder().getType<::mlir::NoneType>())) {
    return ::mlir::failure();
  }
  if (meshAttr) result.getOrAddProperties<AllReduceOp::Properties>().mesh = meshAttr;
  if (::mlir::succeeded(parser.parseOptionalKeyword("mesh_axes"))) {
  if (parser.parseEqual())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(mesh_axesAttr, ::mlir::Type{})) {
    return ::mlir::failure();
  }
  if (mesh_axesAttr) result.getOrAddProperties<AllReduceOp::Properties>().mesh_axes = mesh_axesAttr;
  }
  if (::mlir::succeeded(parser.parseOptionalKeyword("reduction"))) {
  if (parser.parseEqual())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(reductionAttr, ::mlir::Type{})) {
    return ::mlir::failure();
  }
  if (reductionAttr) result.getOrAddProperties<AllReduceOp::Properties>().reduction = reductionAttr;
  }
  {
    auto loc = parser.getCurrentLocation();(void)loc;
    if (parser.parseOptionalAttrDict(result.attributes))
      return ::mlir::failure();
    if (failed(verifyInherentAttrs(result.name, result.attributes, [&]() {
        return parser.emitError(loc) << "'" << result.name.getStringRef() << "' op ";
      })))
      return ::mlir::failure();
  }
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::RankedTensorType type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    inputRawTypes[0] = type;
  }
  if (parser.parseArrow())
    return ::mlir::failure();

  {
    ::mlir::RankedTensorType type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    resultRawTypes[0] = type;
  }
  result.addTypes(resultTypes);
  if (parser.resolveOperands(inputOperands, inputTypes, inputOperandsLoc, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void AllReduceOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  _odsPrinter << getInput();
  _odsPrinter << ' ' << "on";
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(getMeshAttr());
  if (getMeshAxesAttr() && getMeshAxesAttr() != ::mlir::OpBuilder((*this)->getContext()).getDenseI16ArrayAttr({})) {
    _odsPrinter << ' ' << "mesh_axes";
    _odsPrinter << ' ' << "=";
    _odsPrinter << ' ';
  _odsPrinter.printStrippedAttrOrType(getMeshAxesAttr());
  }
  if (getReductionAttr() && getReductionAttr() != ::mlir::mesh::PartialAttr::get(::mlir::OpBuilder((*this)->getContext()).getContext(), ::mlir::mesh::Partial::Sum)) {
    _odsPrinter << ' ' << "reduction";
    _odsPrinter << ' ' << "=";
    _odsPrinter << ' ';
  _odsPrinter.printStrippedAttrOrType(getReductionAttr());
  }
  ::llvm::SmallVector<::llvm::StringRef, 2> elidedAttrs;
  elidedAttrs.push_back("mesh");
  elidedAttrs.push_back("mesh_axes");
  elidedAttrs.push_back("reduction");
  {
     ::mlir::Builder odsBuilder(getContext());
     ::mlir::Attribute attr = getMeshAxesAttr();
     if(attr && (attr == odsBuilder.getDenseI16ArrayAttr({})))
       elidedAttrs.push_back("mesh_axes");
  }
  {
     ::mlir::Builder odsBuilder(getContext());
     ::mlir::Attribute attr = getReductionAttr();
     if(attr && (attr == ::mlir::mesh::PartialAttr::get(odsBuilder.getContext(), ::mlir::mesh::Partial::Sum)))
       elidedAttrs.push_back("reduction");
  }
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), elidedAttrs);
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = getInput().getType();
    if (auto validType = ::llvm::dyn_cast<::mlir::RankedTensorType>(type))
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
  _odsPrinter << ' ' << "->";
  _odsPrinter << ' ';
  {
    auto type = getResult().getType();
    if (auto validType = ::llvm::dyn_cast<::mlir::RankedTensorType>(type))
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

} // namespace mesh
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::mesh::AllReduceOp)

namespace mlir {
namespace mesh {

//===----------------------------------------------------------------------===//
// ::mlir::mesh::AllToAllOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
AllToAllOpGenericAdaptorBase::AllToAllOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, const Properties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), properties(properties), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("mesh.all_to_all", odsAttrs.getContext());
}

AllToAllOpGenericAdaptorBase::AllToAllOpGenericAdaptorBase(AllToAllOp op) : AllToAllOpGenericAdaptorBase(op->getDiscardableAttrDictionary(), op.getProperties(), op->getRegions()) {}

std::pair<unsigned, unsigned> AllToAllOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr AllToAllOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

::mlir::FlatSymbolRefAttr AllToAllOpGenericAdaptorBase::getMeshAttr() {
  auto attr = ::llvm::cast<::mlir::FlatSymbolRefAttr>(getProperties().mesh);
  return attr;
}

::llvm::StringRef AllToAllOpGenericAdaptorBase::getMesh() {
  auto attr = getMeshAttr();
  return attr.getValue();
}

::mlir::DenseI16ArrayAttr AllToAllOpGenericAdaptorBase::getMeshAxesAttr() {
  auto attr = ::llvm::dyn_cast_or_null<::mlir::DenseI16ArrayAttr>(getProperties().mesh_axes);
  return attr;
}

::llvm::ArrayRef<int16_t> AllToAllOpGenericAdaptorBase::getMeshAxes() {
  auto attr = getMeshAxesAttr();
  return attr;
}

::mlir::IntegerAttr AllToAllOpGenericAdaptorBase::getSplitAxisAttr() {
  auto attr = ::llvm::cast<::mlir::IntegerAttr>(getProperties().split_axis);
  return attr;
}

::llvm::APInt AllToAllOpGenericAdaptorBase::getSplitAxis() {
  auto attr = getSplitAxisAttr();
  return attr.getValue();
}

::mlir::IntegerAttr AllToAllOpGenericAdaptorBase::getConcatAxisAttr() {
  auto attr = ::llvm::cast<::mlir::IntegerAttr>(getProperties().concat_axis);
  return attr;
}

::llvm::APInt AllToAllOpGenericAdaptorBase::getConcatAxis() {
  auto attr = getConcatAxisAttr();
  return attr.getValue();
}

} // namespace detail
AllToAllOpAdaptor::AllToAllOpAdaptor(AllToAllOp op) : AllToAllOpGenericAdaptor(op->getOperands(), op) {}

::mlir::LogicalResult AllToAllOpAdaptor::verify(::mlir::Location loc) {
  auto tblgen_concat_axis = getProperties().concat_axis; (void)tblgen_concat_axis;
  if (!tblgen_concat_axis) return emitError(loc, "'mesh.all_to_all' op ""requires attribute 'concat_axis'");
  auto tblgen_mesh = getProperties().mesh; (void)tblgen_mesh;
  if (!tblgen_mesh) return emitError(loc, "'mesh.all_to_all' op ""requires attribute 'mesh'");
  auto tblgen_mesh_axes = getProperties().mesh_axes; (void)tblgen_mesh_axes;
  auto tblgen_split_axis = getProperties().split_axis; (void)tblgen_split_axis;
  if (!tblgen_split_axis) return emitError(loc, "'mesh.all_to_all' op ""requires attribute 'split_axis'");

  if (tblgen_mesh && !((::llvm::isa<::mlir::FlatSymbolRefAttr>(tblgen_mesh))))
    return emitError(loc, "'mesh.all_to_all' op ""attribute 'mesh' failed to satisfy constraint: flat symbol reference attribute");

  if (tblgen_mesh_axes && !((::llvm::isa<::mlir::DenseI16ArrayAttr>(tblgen_mesh_axes))))
    return emitError(loc, "'mesh.all_to_all' op ""attribute 'mesh_axes' failed to satisfy constraint: i16 dense array attribute");

  if (tblgen_split_axis && !(((::llvm::isa<::mlir::IntegerAttr>(tblgen_split_axis))) && ((::llvm::isa<::mlir::IndexType>(::llvm::cast<::mlir::IntegerAttr>(tblgen_split_axis).getType())))))
    return emitError(loc, "'mesh.all_to_all' op ""attribute 'split_axis' failed to satisfy constraint: index attribute");

  if (tblgen_concat_axis && !(((::llvm::isa<::mlir::IntegerAttr>(tblgen_concat_axis))) && ((::llvm::isa<::mlir::IndexType>(::llvm::cast<::mlir::IntegerAttr>(tblgen_concat_axis).getType())))))
    return emitError(loc, "'mesh.all_to_all' op ""attribute 'concat_axis' failed to satisfy constraint: index attribute");
  return ::mlir::success();
}

std::pair<unsigned, unsigned> AllToAllOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range AllToAllOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::TypedValue<::mlir::TensorType> AllToAllOp::getInput() {
  return ::llvm::cast<::mlir::TypedValue<::mlir::TensorType>>(*getODSOperands(0).begin());
}

::mlir::OpOperand &AllToAllOp::getInputMutable() {
  auto range = getODSOperandIndexAndLength(0);
  return getOperation()->getOpOperand(range.first);
}

std::pair<unsigned, unsigned> AllToAllOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range AllToAllOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::TypedValue<::mlir::TensorType> AllToAllOp::getResult() {
  return ::llvm::cast<::mlir::TypedValue<::mlir::TensorType>>(*getODSResults(0).begin());
}

::mlir::LogicalResult AllToAllOp::setPropertiesFromAttr(Properties &prop, ::mlir::Attribute attr, ::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  ::mlir::DictionaryAttr dict = ::llvm::dyn_cast<::mlir::DictionaryAttr>(attr);
  if (!dict) {
    emitError() << "expected DictionaryAttr to set properties";
    return ::mlir::failure();
  }

  {
    auto &propStorage = prop.concat_axis;
       auto attr = dict.get("concat_axis");
    if (attr || /*isRequired=*/true) {
      if (!attr) {
        emitError() << "expected key entry for concat_axis in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `concat_axis` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }

  {
    auto &propStorage = prop.mesh;
       auto attr = dict.get("mesh");
    if (attr || /*isRequired=*/true) {
      if (!attr) {
        emitError() << "expected key entry for mesh in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `mesh` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }

  {
    auto &propStorage = prop.mesh_axes;
       auto attr = dict.get("mesh_axes");
    if (attr || /*isRequired=*/false) {
      if (!attr) {
        emitError() << "expected key entry for mesh_axes in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `mesh_axes` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }

  {
    auto &propStorage = prop.split_axis;
       auto attr = dict.get("split_axis");
    if (attr || /*isRequired=*/true) {
      if (!attr) {
        emitError() << "expected key entry for split_axis in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `split_axis` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }
  return ::mlir::success();
}

::mlir::Attribute AllToAllOp::getPropertiesAsAttr(::mlir::MLIRContext *ctx, const Properties &prop) {
    ::mlir::SmallVector<::mlir::NamedAttribute> attrs;
    ::mlir::Builder odsBuilder{ctx};

    {
      const auto &propStorage = prop.concat_axis;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("concat_axis",
                                       propStorage));
    }

    {
      const auto &propStorage = prop.mesh;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("mesh",
                                       propStorage));
    }

    {
      const auto &propStorage = prop.mesh_axes;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("mesh_axes",
                                       propStorage));
    }

    {
      const auto &propStorage = prop.split_axis;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("split_axis",
                                       propStorage));
    }

  if (!attrs.empty())
    return odsBuilder.getDictionaryAttr(attrs);
  return {};
}

llvm::hash_code AllToAllOp::computePropertiesHash(const Properties &prop) {
  return llvm::hash_combine(
    llvm::hash_value(prop.concat_axis.getAsOpaquePointer()), 
    llvm::hash_value(prop.mesh.getAsOpaquePointer()), 
    llvm::hash_value(prop.mesh_axes.getAsOpaquePointer()), 
    llvm::hash_value(prop.split_axis.getAsOpaquePointer()));
}

std::optional<mlir::Attribute> AllToAllOp::getInherentAttr(::mlir::MLIRContext *ctx, const Properties &prop, llvm::StringRef name) {
    if (name == "concat_axis")
      return prop.concat_axis;

    if (name == "mesh")
      return prop.mesh;

    if (name == "mesh_axes")
      return prop.mesh_axes;

    if (name == "split_axis")
      return prop.split_axis;
  return std::nullopt;
}

void AllToAllOp::setInherentAttr(Properties &prop, llvm::StringRef name, mlir::Attribute value) {
    if (name == "concat_axis") {
       prop.concat_axis = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.concat_axis)>>(value);
       return;
    }

    if (name == "mesh") {
       prop.mesh = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.mesh)>>(value);
       return;
    }

    if (name == "mesh_axes") {
       prop.mesh_axes = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.mesh_axes)>>(value);
       return;
    }

    if (name == "split_axis") {
       prop.split_axis = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.split_axis)>>(value);
       return;
    }
}

void AllToAllOp::populateInherentAttrs(::mlir::MLIRContext *ctx, const Properties &prop, ::mlir::NamedAttrList &attrs) {
    if (prop.concat_axis) attrs.append("concat_axis", prop.concat_axis);

    if (prop.mesh) attrs.append("mesh", prop.mesh);

    if (prop.mesh_axes) attrs.append("mesh_axes", prop.mesh_axes);

    if (prop.split_axis) attrs.append("split_axis", prop.split_axis);
}

::mlir::LogicalResult AllToAllOp::verifyInherentAttrs(::mlir::OperationName opName, ::mlir::NamedAttrList &attrs, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
    {
      ::mlir::Attribute attr = attrs.get(getConcatAxisAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps2(attr, "concat_axis", emitError)))
        return ::mlir::failure();
    }

    {
      ::mlir::Attribute attr = attrs.get(getMeshAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps0(attr, "mesh", emitError)))
        return ::mlir::failure();
    }

    {
      ::mlir::Attribute attr = attrs.get(getMeshAxesAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps1(attr, "mesh_axes", emitError)))
        return ::mlir::failure();
    }

    {
      ::mlir::Attribute attr = attrs.get(getSplitAxisAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps2(attr, "split_axis", emitError)))
        return ::mlir::failure();
    }
    return ::mlir::success();
}

::mlir::LogicalResult AllToAllOp::readProperties(::mlir::DialectBytecodeReader &reader, ::mlir::OperationState &state) {
  auto &prop = state.getOrAddProperties<Properties>(); (void)prop;
  if (::mlir::failed(reader.readAttribute(prop.concat_axis)))
    return ::mlir::failure();

  if (::mlir::failed(reader.readAttribute(prop.mesh)))
    return ::mlir::failure();

  if (::mlir::failed(reader.readOptionalAttribute(prop.mesh_axes)))
    return ::mlir::failure();

  if (::mlir::failed(reader.readAttribute(prop.split_axis)))
    return ::mlir::failure();
  return ::mlir::success();
}

void AllToAllOp::writeProperties(::mlir::DialectBytecodeWriter &writer) {
  auto &prop = getProperties(); (void)prop;
  writer.writeAttribute(prop.concat_axis);
  writer.writeAttribute(prop.mesh);

  writer.writeOptionalAttribute(prop.mesh_axes);
  writer.writeAttribute(prop.split_axis);
}

::mlir::FlatSymbolRefAttr AllToAllOp::getMeshAttr() {
  return ::llvm::cast<::mlir::FlatSymbolRefAttr>(getProperties().mesh);
}

::llvm::StringRef AllToAllOp::getMesh() {
  auto attr = getMeshAttr();
  return attr.getValue();
}

::mlir::DenseI16ArrayAttr AllToAllOp::getMeshAxesAttr() {
  return ::llvm::dyn_cast_or_null<::mlir::DenseI16ArrayAttr>(getProperties().mesh_axes);
}

::llvm::ArrayRef<int16_t> AllToAllOp::getMeshAxes() {
  auto attr = getMeshAxesAttr();
  return attr;
}

::mlir::IntegerAttr AllToAllOp::getSplitAxisAttr() {
  return ::llvm::cast<::mlir::IntegerAttr>(getProperties().split_axis);
}

::llvm::APInt AllToAllOp::getSplitAxis() {
  auto attr = getSplitAxisAttr();
  return attr.getValue();
}

::mlir::IntegerAttr AllToAllOp::getConcatAxisAttr() {
  return ::llvm::cast<::mlir::IntegerAttr>(getProperties().concat_axis);
}

::llvm::APInt AllToAllOp::getConcatAxis() {
  auto attr = getConcatAxisAttr();
  return attr.getValue();
}

void AllToAllOp::setMeshAttr(::mlir::FlatSymbolRefAttr attr) {
  (*this)->setAttr(getMeshAttrName(), attr);
}

void AllToAllOp::setMesh(::llvm::StringRef attrValue) {
  (*this)->setAttr(getMeshAttrName(), ::mlir::SymbolRefAttr::get(::mlir::Builder((*this)->getContext()).getContext(), attrValue));
}

void AllToAllOp::setMeshAxesAttr(::mlir::DenseI16ArrayAttr attr) {
  (*this)->setAttr(getMeshAxesAttrName(), attr);
}

void AllToAllOp::setMeshAxes(::llvm::ArrayRef<int16_t> attrValue) {
  (*this)->setAttr(getMeshAxesAttrName(), ::mlir::Builder((*this)->getContext()).getDenseI16ArrayAttr(attrValue));
}

void AllToAllOp::setSplitAxisAttr(::mlir::IntegerAttr attr) {
  (*this)->setAttr(getSplitAxisAttrName(), attr);
}

void AllToAllOp::setSplitAxis(::llvm::APInt attrValue) {
  (*this)->setAttr(getSplitAxisAttrName(), ::mlir::Builder((*this)->getContext()).getIntegerAttr(::mlir::Builder((*this)->getContext()).getIndexType(), attrValue));
}

void AllToAllOp::setConcatAxisAttr(::mlir::IntegerAttr attr) {
  (*this)->setAttr(getConcatAxisAttrName(), attr);
}

void AllToAllOp::setConcatAxis(::llvm::APInt attrValue) {
  (*this)->setAttr(getConcatAxisAttrName(), ::mlir::Builder((*this)->getContext()).getIntegerAttr(::mlir::Builder((*this)->getContext()).getIndexType(), attrValue));
}

void AllToAllOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::IntegerAttr split_axis, ::mlir::IntegerAttr concat_axis) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = mesh;
  if (mesh_axes) {
    odsState.getOrAddProperties<Properties>().mesh_axes = mesh_axes;
  }
  odsState.getOrAddProperties<Properties>().split_axis = split_axis;
  odsState.getOrAddProperties<Properties>().concat_axis = concat_axis;
  odsState.addTypes(result);
}

void AllToAllOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::IntegerAttr split_axis, ::mlir::IntegerAttr concat_axis) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = mesh;
  if (mesh_axes) {
    odsState.getOrAddProperties<Properties>().mesh_axes = mesh_axes;
  }
  odsState.getOrAddProperties<Properties>().split_axis = split_axis;
  odsState.getOrAddProperties<Properties>().concat_axis = concat_axis;
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void AllToAllOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::llvm::APInt split_axis, ::llvm::APInt concat_axis) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = ::mlir::SymbolRefAttr::get(odsBuilder.getContext(), mesh);
  odsState.getOrAddProperties<Properties>().mesh_axes = odsBuilder.getDenseI16ArrayAttr(mesh_axes);
  odsState.getOrAddProperties<Properties>().split_axis = odsBuilder.getIntegerAttr(odsBuilder.getIndexType(), split_axis);
  odsState.getOrAddProperties<Properties>().concat_axis = odsBuilder.getIntegerAttr(odsBuilder.getIndexType(), concat_axis);
  odsState.addTypes(result);
}

void AllToAllOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::llvm::APInt split_axis, ::llvm::APInt concat_axis) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = ::mlir::SymbolRefAttr::get(odsBuilder.getContext(), mesh);
  odsState.getOrAddProperties<Properties>().mesh_axes = odsBuilder.getDenseI16ArrayAttr(mesh_axes);
  odsState.getOrAddProperties<Properties>().split_axis = odsBuilder.getIntegerAttr(odsBuilder.getIndexType(), split_axis);
  odsState.getOrAddProperties<Properties>().concat_axis = odsBuilder.getIntegerAttr(odsBuilder.getIndexType(), concat_axis);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void AllToAllOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

void AllToAllOp::populateDefaultProperties(::mlir::OperationName opName, Properties &properties) {
  ::mlir::Builder odsBuilder(opName.getContext());
  if (!properties.mesh_axes)
    properties.mesh_axes = odsBuilder.getDenseI16ArrayAttr({});
}

::mlir::LogicalResult AllToAllOp::verifyInvariantsImpl() {
  auto tblgen_concat_axis = getProperties().concat_axis; (void)tblgen_concat_axis;
  if (!tblgen_concat_axis) return emitOpError("requires attribute 'concat_axis'");
  auto tblgen_mesh = getProperties().mesh; (void)tblgen_mesh;
  if (!tblgen_mesh) return emitOpError("requires attribute 'mesh'");
  auto tblgen_mesh_axes = getProperties().mesh_axes; (void)tblgen_mesh_axes;
  auto tblgen_split_axis = getProperties().split_axis; (void)tblgen_split_axis;
  if (!tblgen_split_axis) return emitOpError("requires attribute 'split_axis'");

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps0(*this, tblgen_mesh, "mesh")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps1(*this, tblgen_mesh_axes, "mesh_axes")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps2(*this, tblgen_split_axis, "split_axis")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps2(*this, tblgen_concat_axis, "concat_axis")))
    return ::mlir::failure();
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_MeshOps0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_MeshOps0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult AllToAllOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

::mlir::ParseResult AllToAllOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::UnresolvedOperand inputRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::UnresolvedOperand> inputOperands(inputRawOperands);  ::llvm::SMLoc inputOperandsLoc;
  (void)inputOperandsLoc;
  ::mlir::FlatSymbolRefAttr meshAttr;
  ::mlir::DenseI16ArrayAttr mesh_axesAttr;
  ::mlir::IntegerAttr split_axisAttr;
  ::mlir::IntegerAttr concat_axisAttr;
  ::mlir::Type inputRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> inputTypes(inputRawTypes);
  ::mlir::Type resultRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> resultTypes(resultRawTypes);

  inputOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(inputRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseKeyword("on"))
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(meshAttr, parser.getBuilder().getType<::mlir::NoneType>())) {
    return ::mlir::failure();
  }
  if (meshAttr) result.getOrAddProperties<AllToAllOp::Properties>().mesh = meshAttr;
  if (::mlir::succeeded(parser.parseOptionalKeyword("mesh_axes"))) {
  if (parser.parseEqual())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(mesh_axesAttr, ::mlir::Type{})) {
    return ::mlir::failure();
  }
  if (mesh_axesAttr) result.getOrAddProperties<AllToAllOp::Properties>().mesh_axes = mesh_axesAttr;
  }
  if (parser.parseKeyword("split_axis"))
    return ::mlir::failure();
  if (parser.parseEqual())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(split_axisAttr, parser.getBuilder().getIndexType())) {
    return ::mlir::failure();
  }
  if (split_axisAttr) result.getOrAddProperties<AllToAllOp::Properties>().split_axis = split_axisAttr;
  if (parser.parseKeyword("concat_axis"))
    return ::mlir::failure();
  if (parser.parseEqual())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(concat_axisAttr, parser.getBuilder().getIndexType())) {
    return ::mlir::failure();
  }
  if (concat_axisAttr) result.getOrAddProperties<AllToAllOp::Properties>().concat_axis = concat_axisAttr;
  {
    auto loc = parser.getCurrentLocation();(void)loc;
    if (parser.parseOptionalAttrDict(result.attributes))
      return ::mlir::failure();
    if (failed(verifyInherentAttrs(result.name, result.attributes, [&]() {
        return parser.emitError(loc) << "'" << result.name.getStringRef() << "' op ";
      })))
      return ::mlir::failure();
  }
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::TensorType type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    inputRawTypes[0] = type;
  }
  if (parser.parseArrow())
    return ::mlir::failure();

  {
    ::mlir::TensorType type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    resultRawTypes[0] = type;
  }
  result.addTypes(resultTypes);
  if (parser.resolveOperands(inputOperands, inputTypes, inputOperandsLoc, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void AllToAllOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  _odsPrinter << getInput();
  _odsPrinter << ' ' << "on";
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(getMeshAttr());
  if (getMeshAxesAttr() && getMeshAxesAttr() != ::mlir::OpBuilder((*this)->getContext()).getDenseI16ArrayAttr({})) {
    _odsPrinter << ' ' << "mesh_axes";
    _odsPrinter << ' ' << "=";
    _odsPrinter << ' ';
  _odsPrinter.printStrippedAttrOrType(getMeshAxesAttr());
  }
  _odsPrinter << ' ' << "split_axis";
  _odsPrinter << ' ' << "=";
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(getSplitAxisAttr());
  _odsPrinter << ' ' << "concat_axis";
  _odsPrinter << ' ' << "=";
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(getConcatAxisAttr());
  ::llvm::SmallVector<::llvm::StringRef, 2> elidedAttrs;
  elidedAttrs.push_back("mesh");
  elidedAttrs.push_back("mesh_axes");
  elidedAttrs.push_back("split_axis");
  elidedAttrs.push_back("concat_axis");
  {
     ::mlir::Builder odsBuilder(getContext());
     ::mlir::Attribute attr = getMeshAxesAttr();
     if(attr && (attr == odsBuilder.getDenseI16ArrayAttr({})))
       elidedAttrs.push_back("mesh_axes");
  }
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), elidedAttrs);
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = getInput().getType();
    if (auto validType = ::llvm::dyn_cast<::mlir::TensorType>(type))
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
  _odsPrinter << ' ' << "->";
  _odsPrinter << ' ';
  {
    auto type = getResult().getType();
    if (auto validType = ::llvm::dyn_cast<::mlir::TensorType>(type))
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

} // namespace mesh
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::mesh::AllToAllOp)

namespace mlir {
namespace mesh {

//===----------------------------------------------------------------------===//
// ::mlir::mesh::ClusterOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
ClusterOpGenericAdaptorBase::ClusterOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, const Properties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), properties(properties), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("mesh.cluster", odsAttrs.getContext());
}

ClusterOpGenericAdaptorBase::ClusterOpGenericAdaptorBase(ClusterOp op) : ClusterOpGenericAdaptorBase(op->getDiscardableAttrDictionary(), op.getProperties(), op->getRegions()) {}

std::pair<unsigned, unsigned> ClusterOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr ClusterOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

::mlir::StringAttr ClusterOpGenericAdaptorBase::getSymNameAttr() {
  auto attr = ::llvm::cast<::mlir::StringAttr>(getProperties().sym_name);
  return attr;
}

::llvm::StringRef ClusterOpGenericAdaptorBase::getSymName() {
  auto attr = getSymNameAttr();
  return attr.getValue();
}

::mlir::IntegerAttr ClusterOpGenericAdaptorBase::getRankAttr() {
  auto attr = ::llvm::cast<::mlir::IntegerAttr>(getProperties().rank);
  return attr;
}

uint64_t ClusterOpGenericAdaptorBase::getRank() {
  auto attr = getRankAttr();
  return attr.getValue().getZExtValue();
}

::mlir::DenseI64ArrayAttr ClusterOpGenericAdaptorBase::getDimSizesAttr() {
  auto attr = ::llvm::dyn_cast_or_null<::mlir::DenseI64ArrayAttr>(getProperties().dim_sizes);
  return attr;
}

::llvm::ArrayRef<int64_t> ClusterOpGenericAdaptorBase::getDimSizes() {
  auto attr = getDimSizesAttr();
  return attr;
}

} // namespace detail
ClusterOpAdaptor::ClusterOpAdaptor(ClusterOp op) : ClusterOpGenericAdaptor(op->getOperands(), op) {}

::mlir::LogicalResult ClusterOpAdaptor::verify(::mlir::Location loc) {
  auto tblgen_dim_sizes = getProperties().dim_sizes; (void)tblgen_dim_sizes;
  auto tblgen_rank = getProperties().rank; (void)tblgen_rank;
  if (!tblgen_rank) return emitError(loc, "'mesh.cluster' op ""requires attribute 'rank'");
  auto tblgen_sym_name = getProperties().sym_name; (void)tblgen_sym_name;
  if (!tblgen_sym_name) return emitError(loc, "'mesh.cluster' op ""requires attribute 'sym_name'");

  if (tblgen_sym_name && !((::llvm::isa<::mlir::StringAttr>(tblgen_sym_name))))
    return emitError(loc, "'mesh.cluster' op ""attribute 'sym_name' failed to satisfy constraint: string attribute");

  if (tblgen_rank && !(((::llvm::isa<::mlir::IntegerAttr>(tblgen_rank))) && ((::llvm::cast<::mlir::IntegerAttr>(tblgen_rank).getType().isSignlessInteger(64)))))
    return emitError(loc, "'mesh.cluster' op ""attribute 'rank' failed to satisfy constraint: 64-bit signless integer attribute");

  if (tblgen_dim_sizes && !((::llvm::isa<::mlir::DenseI64ArrayAttr>(tblgen_dim_sizes))))
    return emitError(loc, "'mesh.cluster' op ""attribute 'dim_sizes' failed to satisfy constraint: i64 dense array attribute");
  return ::mlir::success();
}

std::pair<unsigned, unsigned> ClusterOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range ClusterOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> ClusterOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range ClusterOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::LogicalResult ClusterOp::setPropertiesFromAttr(Properties &prop, ::mlir::Attribute attr, ::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  ::mlir::DictionaryAttr dict = ::llvm::dyn_cast<::mlir::DictionaryAttr>(attr);
  if (!dict) {
    emitError() << "expected DictionaryAttr to set properties";
    return ::mlir::failure();
  }

  {
    auto &propStorage = prop.dim_sizes;
       auto attr = dict.get("dim_sizes");
    if (attr || /*isRequired=*/false) {
      if (!attr) {
        emitError() << "expected key entry for dim_sizes in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `dim_sizes` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }

  {
    auto &propStorage = prop.rank;
       auto attr = dict.get("rank");
    if (attr || /*isRequired=*/true) {
      if (!attr) {
        emitError() << "expected key entry for rank in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `rank` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }

  {
    auto &propStorage = prop.sym_name;
       auto attr = dict.get("sym_name");
    if (attr || /*isRequired=*/true) {
      if (!attr) {
        emitError() << "expected key entry for sym_name in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `sym_name` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }
  return ::mlir::success();
}

::mlir::Attribute ClusterOp::getPropertiesAsAttr(::mlir::MLIRContext *ctx, const Properties &prop) {
    ::mlir::SmallVector<::mlir::NamedAttribute> attrs;
    ::mlir::Builder odsBuilder{ctx};

    {
      const auto &propStorage = prop.dim_sizes;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("dim_sizes",
                                       propStorage));
    }

    {
      const auto &propStorage = prop.rank;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("rank",
                                       propStorage));
    }

    {
      const auto &propStorage = prop.sym_name;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("sym_name",
                                       propStorage));
    }

  if (!attrs.empty())
    return odsBuilder.getDictionaryAttr(attrs);
  return {};
}

llvm::hash_code ClusterOp::computePropertiesHash(const Properties &prop) {
  return llvm::hash_combine(
    llvm::hash_value(prop.dim_sizes.getAsOpaquePointer()), 
    llvm::hash_value(prop.rank.getAsOpaquePointer()), 
    llvm::hash_value(prop.sym_name.getAsOpaquePointer()));
}

std::optional<mlir::Attribute> ClusterOp::getInherentAttr(::mlir::MLIRContext *ctx, const Properties &prop, llvm::StringRef name) {
    if (name == "dim_sizes")
      return prop.dim_sizes;

    if (name == "rank")
      return prop.rank;

    if (name == "sym_name")
      return prop.sym_name;
  return std::nullopt;
}

void ClusterOp::setInherentAttr(Properties &prop, llvm::StringRef name, mlir::Attribute value) {
    if (name == "dim_sizes") {
       prop.dim_sizes = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.dim_sizes)>>(value);
       return;
    }

    if (name == "rank") {
       prop.rank = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.rank)>>(value);
       return;
    }

    if (name == "sym_name") {
       prop.sym_name = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.sym_name)>>(value);
       return;
    }
}

void ClusterOp::populateInherentAttrs(::mlir::MLIRContext *ctx, const Properties &prop, ::mlir::NamedAttrList &attrs) {
    if (prop.dim_sizes) attrs.append("dim_sizes", prop.dim_sizes);

    if (prop.rank) attrs.append("rank", prop.rank);

    if (prop.sym_name) attrs.append("sym_name", prop.sym_name);
}

::mlir::LogicalResult ClusterOp::verifyInherentAttrs(::mlir::OperationName opName, ::mlir::NamedAttrList &attrs, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
    {
      ::mlir::Attribute attr = attrs.get(getDimSizesAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps6(attr, "dim_sizes", emitError)))
        return ::mlir::failure();
    }

    {
      ::mlir::Attribute attr = attrs.get(getRankAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps5(attr, "rank", emitError)))
        return ::mlir::failure();
    }

    {
      ::mlir::Attribute attr = attrs.get(getSymNameAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps4(attr, "sym_name", emitError)))
        return ::mlir::failure();
    }
    return ::mlir::success();
}

::mlir::LogicalResult ClusterOp::readProperties(::mlir::DialectBytecodeReader &reader, ::mlir::OperationState &state) {
  auto &prop = state.getOrAddProperties<Properties>(); (void)prop;
  if (::mlir::failed(reader.readOptionalAttribute(prop.dim_sizes)))
    return ::mlir::failure();

  if (::mlir::failed(reader.readAttribute(prop.rank)))
    return ::mlir::failure();

  if (::mlir::failed(reader.readAttribute(prop.sym_name)))
    return ::mlir::failure();
  return ::mlir::success();
}

void ClusterOp::writeProperties(::mlir::DialectBytecodeWriter &writer) {
  auto &prop = getProperties(); (void)prop;

  writer.writeOptionalAttribute(prop.dim_sizes);
  writer.writeAttribute(prop.rank);
  writer.writeAttribute(prop.sym_name);
}

::mlir::StringAttr ClusterOp::getSymNameAttr() {
  return ::llvm::cast<::mlir::StringAttr>(getProperties().sym_name);
}

::llvm::StringRef ClusterOp::getSymName() {
  auto attr = getSymNameAttr();
  return attr.getValue();
}

::mlir::IntegerAttr ClusterOp::getRankAttr() {
  return ::llvm::cast<::mlir::IntegerAttr>(getProperties().rank);
}

uint64_t ClusterOp::getRank() {
  auto attr = getRankAttr();
  return attr.getValue().getZExtValue();
}

::mlir::DenseI64ArrayAttr ClusterOp::getDimSizesAttr() {
  return ::llvm::dyn_cast_or_null<::mlir::DenseI64ArrayAttr>(getProperties().dim_sizes);
}

::llvm::ArrayRef<int64_t> ClusterOp::getDimSizes() {
  auto attr = getDimSizesAttr();
  return attr;
}

void ClusterOp::setSymNameAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(getSymNameAttrName(), attr);
}

void ClusterOp::setSymName(::llvm::StringRef attrValue) {
  (*this)->setAttr(getSymNameAttrName(), ::mlir::Builder((*this)->getContext()).getStringAttr(attrValue));
}

void ClusterOp::setRankAttr(::mlir::IntegerAttr attr) {
  (*this)->setAttr(getRankAttrName(), attr);
}

void ClusterOp::setRank(uint64_t attrValue) {
  (*this)->setAttr(getRankAttrName(), ::mlir::Builder((*this)->getContext()).getIntegerAttr(::mlir::Builder((*this)->getContext()).getIntegerType(64), attrValue));
}

void ClusterOp::setDimSizesAttr(::mlir::DenseI64ArrayAttr attr) {
  (*this)->setAttr(getDimSizesAttrName(), attr);
}

void ClusterOp::setDimSizes(::llvm::ArrayRef<int64_t> attrValue) {
  (*this)->setAttr(getDimSizesAttrName(), ::mlir::Builder((*this)->getContext()).getDenseI64ArrayAttr(attrValue));
}

void ClusterOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::StringAttr sym_name, ::mlir::IntegerAttr rank, ::mlir::DenseI64ArrayAttr dim_sizes) {
  odsState.getOrAddProperties<Properties>().sym_name = sym_name;
  odsState.getOrAddProperties<Properties>().rank = rank;
  if (dim_sizes) {
    odsState.getOrAddProperties<Properties>().dim_sizes = dim_sizes;
  }
}

void ClusterOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::StringAttr sym_name, ::mlir::IntegerAttr rank, ::mlir::DenseI64ArrayAttr dim_sizes) {
  odsState.getOrAddProperties<Properties>().sym_name = sym_name;
  odsState.getOrAddProperties<Properties>().rank = rank;
  if (dim_sizes) {
    odsState.getOrAddProperties<Properties>().dim_sizes = dim_sizes;
  }
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void ClusterOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::llvm::StringRef sym_name, uint64_t rank, ::llvm::ArrayRef<int64_t> dim_sizes) {
  odsState.getOrAddProperties<Properties>().sym_name = odsBuilder.getStringAttr(sym_name);
  odsState.getOrAddProperties<Properties>().rank = odsBuilder.getIntegerAttr(odsBuilder.getIntegerType(64), rank);
  odsState.getOrAddProperties<Properties>().dim_sizes = odsBuilder.getDenseI64ArrayAttr(dim_sizes);
}

void ClusterOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef sym_name, uint64_t rank, ::llvm::ArrayRef<int64_t> dim_sizes) {
  odsState.getOrAddProperties<Properties>().sym_name = odsBuilder.getStringAttr(sym_name);
  odsState.getOrAddProperties<Properties>().rank = odsBuilder.getIntegerAttr(odsBuilder.getIntegerType(64), rank);
  odsState.getOrAddProperties<Properties>().dim_sizes = odsBuilder.getDenseI64ArrayAttr(dim_sizes);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void ClusterOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

void ClusterOp::populateDefaultProperties(::mlir::OperationName opName, Properties &properties) {
  ::mlir::Builder odsBuilder(opName.getContext());
  if (!properties.dim_sizes)
    properties.dim_sizes = odsBuilder.getDenseI64ArrayAttr({});
}

::mlir::LogicalResult ClusterOp::verifyInvariantsImpl() {
  auto tblgen_dim_sizes = getProperties().dim_sizes; (void)tblgen_dim_sizes;
  auto tblgen_rank = getProperties().rank; (void)tblgen_rank;
  if (!tblgen_rank) return emitOpError("requires attribute 'rank'");
  auto tblgen_sym_name = getProperties().sym_name; (void)tblgen_sym_name;
  if (!tblgen_sym_name) return emitOpError("requires attribute 'sym_name'");

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps4(*this, tblgen_sym_name, "sym_name")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps5(*this, tblgen_rank, "rank")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps6(*this, tblgen_dim_sizes, "dim_sizes")))
    return ::mlir::failure();
  return ::mlir::success();
}

::mlir::LogicalResult ClusterOp::verifyInvariants() {
  if(::mlir::succeeded(verifyInvariantsImpl()) && ::mlir::succeeded(verify()))
    return ::mlir::success();
  return ::mlir::failure();
}

::mlir::ParseResult ClusterOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::StringAttr sym_nameAttr;
  ::mlir::IntegerAttr rankAttr;
  ::mlir::DenseI64ArrayAttr dim_sizesAttr;

  if (parser.parseSymbolName(sym_nameAttr))
    return ::mlir::failure();
  if (sym_nameAttr) result.getOrAddProperties<ClusterOp::Properties>().sym_name = sym_nameAttr;
  if (parser.parseLParen())
    return ::mlir::failure();
  if (parser.parseKeyword("rank"))
    return ::mlir::failure();
  if (parser.parseEqual())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(rankAttr, parser.getBuilder().getIntegerType(64))) {
    return ::mlir::failure();
  }
  if (rankAttr) result.getOrAddProperties<ClusterOp::Properties>().rank = rankAttr;
  if (::mlir::succeeded(parser.parseOptionalComma())) {
  if (parser.parseKeyword("dim_sizes"))
    return ::mlir::failure();
  if (parser.parseEqual())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(dim_sizesAttr, ::mlir::Type{})) {
    return ::mlir::failure();
  }
  if (dim_sizesAttr) result.getOrAddProperties<ClusterOp::Properties>().dim_sizes = dim_sizesAttr;
  }
  if (parser.parseRParen())
    return ::mlir::failure();
  {
    auto loc = parser.getCurrentLocation();(void)loc;
    if (parser.parseOptionalAttrDict(result.attributes))
      return ::mlir::failure();
    if (failed(verifyInherentAttrs(result.name, result.attributes, [&]() {
        return parser.emitError(loc) << "'" << result.name.getStringRef() << "' op ";
      })))
      return ::mlir::failure();
  }
  return ::mlir::success();
}

void ClusterOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  _odsPrinter.printSymbolName(getSymNameAttr().getValue());
  _odsPrinter << "(";
  _odsPrinter << "rank";
  _odsPrinter << ' ' << "=";
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(getRankAttr());
  if (getDimSizesAttr() && getDimSizesAttr() != ::mlir::OpBuilder((*this)->getContext()).getDenseI64ArrayAttr({})) {
    _odsPrinter << ",";
    _odsPrinter << ' ' << "dim_sizes";
    _odsPrinter << ' ' << "=";
    _odsPrinter << ' ';
  _odsPrinter.printStrippedAttrOrType(getDimSizesAttr());
  }
  _odsPrinter << ")";
  ::llvm::SmallVector<::llvm::StringRef, 2> elidedAttrs;
  elidedAttrs.push_back("sym_name");
  elidedAttrs.push_back("rank");
  elidedAttrs.push_back("dim_sizes");
  {
     ::mlir::Builder odsBuilder(getContext());
     ::mlir::Attribute attr = getDimSizesAttr();
     if(attr && (attr == odsBuilder.getDenseI64ArrayAttr({})))
       elidedAttrs.push_back("dim_sizes");
  }
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), elidedAttrs);
}

} // namespace mesh
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::mesh::ClusterOp)

namespace mlir {
namespace mesh {

//===----------------------------------------------------------------------===//
// ::mlir::mesh::ReduceScatterOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
ReduceScatterOpGenericAdaptorBase::ReduceScatterOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, const Properties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), properties(properties), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("mesh.reduce_scatter", odsAttrs.getContext());
}

ReduceScatterOpGenericAdaptorBase::ReduceScatterOpGenericAdaptorBase(ReduceScatterOp op) : ReduceScatterOpGenericAdaptorBase(op->getDiscardableAttrDictionary(), op.getProperties(), op->getRegions()) {}

std::pair<unsigned, unsigned> ReduceScatterOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr ReduceScatterOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

::mlir::FlatSymbolRefAttr ReduceScatterOpGenericAdaptorBase::getMeshAttr() {
  auto attr = ::llvm::cast<::mlir::FlatSymbolRefAttr>(getProperties().mesh);
  return attr;
}

::llvm::StringRef ReduceScatterOpGenericAdaptorBase::getMesh() {
  auto attr = getMeshAttr();
  return attr.getValue();
}

::mlir::DenseI16ArrayAttr ReduceScatterOpGenericAdaptorBase::getMeshAxesAttr() {
  auto attr = ::llvm::dyn_cast_or_null<::mlir::DenseI16ArrayAttr>(getProperties().mesh_axes);
  return attr;
}

::llvm::ArrayRef<int16_t> ReduceScatterOpGenericAdaptorBase::getMeshAxes() {
  auto attr = getMeshAxesAttr();
  return attr;
}

::mlir::mesh::PartialAttr ReduceScatterOpGenericAdaptorBase::getReductionAttr() {
  auto attr = ::llvm::dyn_cast_or_null<::mlir::mesh::PartialAttr>(getProperties().reduction);
  return attr;
}

::mlir::mesh::Partial ReduceScatterOpGenericAdaptorBase::getReduction() {
  auto attr = getReductionAttr();
  return attr.getValue();
}

::mlir::IntegerAttr ReduceScatterOpGenericAdaptorBase::getScatterAxisAttr() {
  auto attr = ::llvm::cast<::mlir::IntegerAttr>(getProperties().scatter_axis);
  return attr;
}

::llvm::APInt ReduceScatterOpGenericAdaptorBase::getScatterAxis() {
  auto attr = getScatterAxisAttr();
  return attr.getValue();
}

} // namespace detail
ReduceScatterOpAdaptor::ReduceScatterOpAdaptor(ReduceScatterOp op) : ReduceScatterOpGenericAdaptor(op->getOperands(), op) {}

::mlir::LogicalResult ReduceScatterOpAdaptor::verify(::mlir::Location loc) {
  auto tblgen_mesh = getProperties().mesh; (void)tblgen_mesh;
  if (!tblgen_mesh) return emitError(loc, "'mesh.reduce_scatter' op ""requires attribute 'mesh'");
  auto tblgen_mesh_axes = getProperties().mesh_axes; (void)tblgen_mesh_axes;
  auto tblgen_reduction = getProperties().reduction; (void)tblgen_reduction;
  auto tblgen_scatter_axis = getProperties().scatter_axis; (void)tblgen_scatter_axis;
  if (!tblgen_scatter_axis) return emitError(loc, "'mesh.reduce_scatter' op ""requires attribute 'scatter_axis'");

  if (tblgen_mesh && !((::llvm::isa<::mlir::FlatSymbolRefAttr>(tblgen_mesh))))
    return emitError(loc, "'mesh.reduce_scatter' op ""attribute 'mesh' failed to satisfy constraint: flat symbol reference attribute");

  if (tblgen_mesh_axes && !((::llvm::isa<::mlir::DenseI16ArrayAttr>(tblgen_mesh_axes))))
    return emitError(loc, "'mesh.reduce_scatter' op ""attribute 'mesh_axes' failed to satisfy constraint: i16 dense array attribute");

  if (tblgen_reduction && !((::llvm::isa<::mlir::mesh::PartialAttr>(tblgen_reduction))))
    return emitError(loc, "'mesh.reduce_scatter' op ""attribute 'reduction' failed to satisfy constraint: partial type of a distributed tensor");

  if (tblgen_scatter_axis && !(((::llvm::isa<::mlir::IntegerAttr>(tblgen_scatter_axis))) && ((::llvm::isa<::mlir::IndexType>(::llvm::cast<::mlir::IntegerAttr>(tblgen_scatter_axis).getType())))))
    return emitError(loc, "'mesh.reduce_scatter' op ""attribute 'scatter_axis' failed to satisfy constraint: index attribute");
  return ::mlir::success();
}

std::pair<unsigned, unsigned> ReduceScatterOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range ReduceScatterOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::TypedValue<::mlir::TensorType> ReduceScatterOp::getInput() {
  return ::llvm::cast<::mlir::TypedValue<::mlir::TensorType>>(*getODSOperands(0).begin());
}

::mlir::OpOperand &ReduceScatterOp::getInputMutable() {
  auto range = getODSOperandIndexAndLength(0);
  return getOperation()->getOpOperand(range.first);
}

std::pair<unsigned, unsigned> ReduceScatterOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range ReduceScatterOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::TypedValue<::mlir::RankedTensorType> ReduceScatterOp::getResult() {
  return ::llvm::cast<::mlir::TypedValue<::mlir::RankedTensorType>>(*getODSResults(0).begin());
}

::mlir::LogicalResult ReduceScatterOp::setPropertiesFromAttr(Properties &prop, ::mlir::Attribute attr, ::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  ::mlir::DictionaryAttr dict = ::llvm::dyn_cast<::mlir::DictionaryAttr>(attr);
  if (!dict) {
    emitError() << "expected DictionaryAttr to set properties";
    return ::mlir::failure();
  }

  {
    auto &propStorage = prop.mesh;
       auto attr = dict.get("mesh");
    if (attr || /*isRequired=*/true) {
      if (!attr) {
        emitError() << "expected key entry for mesh in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `mesh` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }

  {
    auto &propStorage = prop.mesh_axes;
       auto attr = dict.get("mesh_axes");
    if (attr || /*isRequired=*/false) {
      if (!attr) {
        emitError() << "expected key entry for mesh_axes in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `mesh_axes` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }

  {
    auto &propStorage = prop.reduction;
       auto attr = dict.get("reduction");
    if (attr || /*isRequired=*/false) {
      if (!attr) {
        emitError() << "expected key entry for reduction in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `reduction` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }

  {
    auto &propStorage = prop.scatter_axis;
       auto attr = dict.get("scatter_axis");
    if (attr || /*isRequired=*/true) {
      if (!attr) {
        emitError() << "expected key entry for scatter_axis in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `scatter_axis` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }
  return ::mlir::success();
}

::mlir::Attribute ReduceScatterOp::getPropertiesAsAttr(::mlir::MLIRContext *ctx, const Properties &prop) {
    ::mlir::SmallVector<::mlir::NamedAttribute> attrs;
    ::mlir::Builder odsBuilder{ctx};

    {
      const auto &propStorage = prop.mesh;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("mesh",
                                       propStorage));
    }

    {
      const auto &propStorage = prop.mesh_axes;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("mesh_axes",
                                       propStorage));
    }

    {
      const auto &propStorage = prop.reduction;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("reduction",
                                       propStorage));
    }

    {
      const auto &propStorage = prop.scatter_axis;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("scatter_axis",
                                       propStorage));
    }

  if (!attrs.empty())
    return odsBuilder.getDictionaryAttr(attrs);
  return {};
}

llvm::hash_code ReduceScatterOp::computePropertiesHash(const Properties &prop) {
  return llvm::hash_combine(
    llvm::hash_value(prop.mesh.getAsOpaquePointer()), 
    llvm::hash_value(prop.mesh_axes.getAsOpaquePointer()), 
    llvm::hash_value(prop.reduction.getAsOpaquePointer()), 
    llvm::hash_value(prop.scatter_axis.getAsOpaquePointer()));
}

std::optional<mlir::Attribute> ReduceScatterOp::getInherentAttr(::mlir::MLIRContext *ctx, const Properties &prop, llvm::StringRef name) {
    if (name == "mesh")
      return prop.mesh;

    if (name == "mesh_axes")
      return prop.mesh_axes;

    if (name == "reduction")
      return prop.reduction;

    if (name == "scatter_axis")
      return prop.scatter_axis;
  return std::nullopt;
}

void ReduceScatterOp::setInherentAttr(Properties &prop, llvm::StringRef name, mlir::Attribute value) {
    if (name == "mesh") {
       prop.mesh = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.mesh)>>(value);
       return;
    }

    if (name == "mesh_axes") {
       prop.mesh_axes = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.mesh_axes)>>(value);
       return;
    }

    if (name == "reduction") {
       prop.reduction = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.reduction)>>(value);
       return;
    }

    if (name == "scatter_axis") {
       prop.scatter_axis = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.scatter_axis)>>(value);
       return;
    }
}

void ReduceScatterOp::populateInherentAttrs(::mlir::MLIRContext *ctx, const Properties &prop, ::mlir::NamedAttrList &attrs) {
    if (prop.mesh) attrs.append("mesh", prop.mesh);

    if (prop.mesh_axes) attrs.append("mesh_axes", prop.mesh_axes);

    if (prop.reduction) attrs.append("reduction", prop.reduction);

    if (prop.scatter_axis) attrs.append("scatter_axis", prop.scatter_axis);
}

::mlir::LogicalResult ReduceScatterOp::verifyInherentAttrs(::mlir::OperationName opName, ::mlir::NamedAttrList &attrs, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
    {
      ::mlir::Attribute attr = attrs.get(getMeshAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps0(attr, "mesh", emitError)))
        return ::mlir::failure();
    }

    {
      ::mlir::Attribute attr = attrs.get(getMeshAxesAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps1(attr, "mesh_axes", emitError)))
        return ::mlir::failure();
    }

    {
      ::mlir::Attribute attr = attrs.get(getReductionAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps3(attr, "reduction", emitError)))
        return ::mlir::failure();
    }

    {
      ::mlir::Attribute attr = attrs.get(getScatterAxisAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps2(attr, "scatter_axis", emitError)))
        return ::mlir::failure();
    }
    return ::mlir::success();
}

::mlir::LogicalResult ReduceScatterOp::readProperties(::mlir::DialectBytecodeReader &reader, ::mlir::OperationState &state) {
  auto &prop = state.getOrAddProperties<Properties>(); (void)prop;
  if (::mlir::failed(reader.readAttribute(prop.mesh)))
    return ::mlir::failure();

  if (::mlir::failed(reader.readOptionalAttribute(prop.mesh_axes)))
    return ::mlir::failure();

  if (::mlir::failed(reader.readOptionalAttribute(prop.reduction)))
    return ::mlir::failure();

  if (::mlir::failed(reader.readAttribute(prop.scatter_axis)))
    return ::mlir::failure();
  return ::mlir::success();
}

void ReduceScatterOp::writeProperties(::mlir::DialectBytecodeWriter &writer) {
  auto &prop = getProperties(); (void)prop;
  writer.writeAttribute(prop.mesh);

  writer.writeOptionalAttribute(prop.mesh_axes);

  writer.writeOptionalAttribute(prop.reduction);
  writer.writeAttribute(prop.scatter_axis);
}

::mlir::FlatSymbolRefAttr ReduceScatterOp::getMeshAttr() {
  return ::llvm::cast<::mlir::FlatSymbolRefAttr>(getProperties().mesh);
}

::llvm::StringRef ReduceScatterOp::getMesh() {
  auto attr = getMeshAttr();
  return attr.getValue();
}

::mlir::DenseI16ArrayAttr ReduceScatterOp::getMeshAxesAttr() {
  return ::llvm::dyn_cast_or_null<::mlir::DenseI16ArrayAttr>(getProperties().mesh_axes);
}

::llvm::ArrayRef<int16_t> ReduceScatterOp::getMeshAxes() {
  auto attr = getMeshAxesAttr();
  return attr;
}

::mlir::mesh::PartialAttr ReduceScatterOp::getReductionAttr() {
  return ::llvm::dyn_cast_or_null<::mlir::mesh::PartialAttr>(getProperties().reduction);
}

::mlir::mesh::Partial ReduceScatterOp::getReduction() {
  auto attr = getReductionAttr();
  return attr.getValue();
}

::mlir::IntegerAttr ReduceScatterOp::getScatterAxisAttr() {
  return ::llvm::cast<::mlir::IntegerAttr>(getProperties().scatter_axis);
}

::llvm::APInt ReduceScatterOp::getScatterAxis() {
  auto attr = getScatterAxisAttr();
  return attr.getValue();
}

void ReduceScatterOp::setMeshAttr(::mlir::FlatSymbolRefAttr attr) {
  (*this)->setAttr(getMeshAttrName(), attr);
}

void ReduceScatterOp::setMesh(::llvm::StringRef attrValue) {
  (*this)->setAttr(getMeshAttrName(), ::mlir::SymbolRefAttr::get(::mlir::Builder((*this)->getContext()).getContext(), attrValue));
}

void ReduceScatterOp::setMeshAxesAttr(::mlir::DenseI16ArrayAttr attr) {
  (*this)->setAttr(getMeshAxesAttrName(), attr);
}

void ReduceScatterOp::setMeshAxes(::llvm::ArrayRef<int16_t> attrValue) {
  (*this)->setAttr(getMeshAxesAttrName(), ::mlir::Builder((*this)->getContext()).getDenseI16ArrayAttr(attrValue));
}

void ReduceScatterOp::setReductionAttr(::mlir::mesh::PartialAttr attr) {
  (*this)->setAttr(getReductionAttrName(), attr);
}

void ReduceScatterOp::setReduction(::mlir::mesh::Partial attrValue) {
  (*this)->setAttr(getReductionAttrName(), ::mlir::mesh::PartialAttr::get(::mlir::Builder((*this)->getContext()).getContext(), attrValue));
}

void ReduceScatterOp::setScatterAxisAttr(::mlir::IntegerAttr attr) {
  (*this)->setAttr(getScatterAxisAttrName(), attr);
}

void ReduceScatterOp::setScatterAxis(::llvm::APInt attrValue) {
  (*this)->setAttr(getScatterAxisAttrName(), ::mlir::Builder((*this)->getContext()).getIntegerAttr(::mlir::Builder((*this)->getContext()).getIndexType(), attrValue));
}

void ReduceScatterOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::mesh::PartialAttr reduction, ::mlir::IntegerAttr scatter_axis) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = mesh;
  if (mesh_axes) {
    odsState.getOrAddProperties<Properties>().mesh_axes = mesh_axes;
  }
  if (reduction) {
    odsState.getOrAddProperties<Properties>().reduction = reduction;
  }
  odsState.getOrAddProperties<Properties>().scatter_axis = scatter_axis;
  odsState.addTypes(result);
}

void ReduceScatterOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::mesh::PartialAttr reduction, ::mlir::IntegerAttr scatter_axis) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = mesh;
  if (mesh_axes) {
    odsState.getOrAddProperties<Properties>().mesh_axes = mesh_axes;
  }
  if (reduction) {
    odsState.getOrAddProperties<Properties>().reduction = reduction;
  }
  odsState.getOrAddProperties<Properties>().scatter_axis = scatter_axis;
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void ReduceScatterOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::mlir::mesh::Partial reduction, ::llvm::APInt scatter_axis) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = ::mlir::SymbolRefAttr::get(odsBuilder.getContext(), mesh);
  odsState.getOrAddProperties<Properties>().mesh_axes = odsBuilder.getDenseI16ArrayAttr(mesh_axes);
  odsState.getOrAddProperties<Properties>().reduction = ::mlir::mesh::PartialAttr::get(odsBuilder.getContext(), reduction);
  odsState.getOrAddProperties<Properties>().scatter_axis = odsBuilder.getIntegerAttr(odsBuilder.getIndexType(), scatter_axis);
  odsState.addTypes(result);
}

void ReduceScatterOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::mlir::mesh::Partial reduction, ::llvm::APInt scatter_axis) {
  odsState.addOperands(input);
  odsState.getOrAddProperties<Properties>().mesh = ::mlir::SymbolRefAttr::get(odsBuilder.getContext(), mesh);
  odsState.getOrAddProperties<Properties>().mesh_axes = odsBuilder.getDenseI16ArrayAttr(mesh_axes);
  odsState.getOrAddProperties<Properties>().reduction = ::mlir::mesh::PartialAttr::get(odsBuilder.getContext(), reduction);
  odsState.getOrAddProperties<Properties>().scatter_axis = odsBuilder.getIntegerAttr(odsBuilder.getIndexType(), scatter_axis);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void ReduceScatterOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

void ReduceScatterOp::populateDefaultProperties(::mlir::OperationName opName, Properties &properties) {
  ::mlir::Builder odsBuilder(opName.getContext());
  if (!properties.mesh_axes)
    properties.mesh_axes = odsBuilder.getDenseI16ArrayAttr({});
  if (!properties.reduction)
    properties.reduction = ::mlir::mesh::PartialAttr::get(odsBuilder.getContext(), ::mlir::mesh::Partial::Sum);
}

::mlir::LogicalResult ReduceScatterOp::verifyInvariantsImpl() {
  auto tblgen_mesh = getProperties().mesh; (void)tblgen_mesh;
  if (!tblgen_mesh) return emitOpError("requires attribute 'mesh'");
  auto tblgen_mesh_axes = getProperties().mesh_axes; (void)tblgen_mesh_axes;
  auto tblgen_reduction = getProperties().reduction; (void)tblgen_reduction;
  auto tblgen_scatter_axis = getProperties().scatter_axis; (void)tblgen_scatter_axis;
  if (!tblgen_scatter_axis) return emitOpError("requires attribute 'scatter_axis'");

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps0(*this, tblgen_mesh, "mesh")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps1(*this, tblgen_mesh_axes, "mesh_axes")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps3(*this, tblgen_reduction, "reduction")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps2(*this, tblgen_scatter_axis, "scatter_axis")))
    return ::mlir::failure();
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_MeshOps0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_MeshOps1(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult ReduceScatterOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

::mlir::ParseResult ReduceScatterOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::UnresolvedOperand inputRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::UnresolvedOperand> inputOperands(inputRawOperands);  ::llvm::SMLoc inputOperandsLoc;
  (void)inputOperandsLoc;
  ::mlir::FlatSymbolRefAttr meshAttr;
  ::mlir::DenseI16ArrayAttr mesh_axesAttr;
  ::mlir::mesh::PartialAttr reductionAttr;
  ::mlir::IntegerAttr scatter_axisAttr;
  ::mlir::Type inputRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> inputTypes(inputRawTypes);
  ::mlir::Type resultRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> resultTypes(resultRawTypes);

  inputOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(inputRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseKeyword("on"))
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(meshAttr, parser.getBuilder().getType<::mlir::NoneType>())) {
    return ::mlir::failure();
  }
  if (meshAttr) result.getOrAddProperties<ReduceScatterOp::Properties>().mesh = meshAttr;
  if (::mlir::succeeded(parser.parseOptionalKeyword("mesh_axes"))) {
  if (parser.parseEqual())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(mesh_axesAttr, ::mlir::Type{})) {
    return ::mlir::failure();
  }
  if (mesh_axesAttr) result.getOrAddProperties<ReduceScatterOp::Properties>().mesh_axes = mesh_axesAttr;
  }
  if (::mlir::succeeded(parser.parseOptionalKeyword("reduction"))) {
  if (parser.parseEqual())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(reductionAttr, ::mlir::Type{})) {
    return ::mlir::failure();
  }
  if (reductionAttr) result.getOrAddProperties<ReduceScatterOp::Properties>().reduction = reductionAttr;
  }
  if (parser.parseKeyword("scatter_axis"))
    return ::mlir::failure();
  if (parser.parseEqual())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(scatter_axisAttr, parser.getBuilder().getIndexType())) {
    return ::mlir::failure();
  }
  if (scatter_axisAttr) result.getOrAddProperties<ReduceScatterOp::Properties>().scatter_axis = scatter_axisAttr;
  {
    auto loc = parser.getCurrentLocation();(void)loc;
    if (parser.parseOptionalAttrDict(result.attributes))
      return ::mlir::failure();
    if (failed(verifyInherentAttrs(result.name, result.attributes, [&]() {
        return parser.emitError(loc) << "'" << result.name.getStringRef() << "' op ";
      })))
      return ::mlir::failure();
  }
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::TensorType type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    inputRawTypes[0] = type;
  }
  if (parser.parseArrow())
    return ::mlir::failure();

  {
    ::mlir::RankedTensorType type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    resultRawTypes[0] = type;
  }
  result.addTypes(resultTypes);
  if (parser.resolveOperands(inputOperands, inputTypes, inputOperandsLoc, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void ReduceScatterOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  _odsPrinter << getInput();
  _odsPrinter << ' ' << "on";
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(getMeshAttr());
  if (getMeshAxesAttr() && getMeshAxesAttr() != ::mlir::OpBuilder((*this)->getContext()).getDenseI16ArrayAttr({})) {
    _odsPrinter << ' ' << "mesh_axes";
    _odsPrinter << ' ' << "=";
    _odsPrinter << ' ';
  _odsPrinter.printStrippedAttrOrType(getMeshAxesAttr());
  }
  if (getReductionAttr() && getReductionAttr() != ::mlir::mesh::PartialAttr::get(::mlir::OpBuilder((*this)->getContext()).getContext(), ::mlir::mesh::Partial::Sum)) {
    _odsPrinter << ' ' << "reduction";
    _odsPrinter << ' ' << "=";
    _odsPrinter << ' ';
  _odsPrinter.printStrippedAttrOrType(getReductionAttr());
  }
  _odsPrinter << ' ' << "scatter_axis";
  _odsPrinter << ' ' << "=";
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(getScatterAxisAttr());
  ::llvm::SmallVector<::llvm::StringRef, 2> elidedAttrs;
  elidedAttrs.push_back("mesh");
  elidedAttrs.push_back("mesh_axes");
  elidedAttrs.push_back("reduction");
  elidedAttrs.push_back("scatter_axis");
  {
     ::mlir::Builder odsBuilder(getContext());
     ::mlir::Attribute attr = getMeshAxesAttr();
     if(attr && (attr == odsBuilder.getDenseI16ArrayAttr({})))
       elidedAttrs.push_back("mesh_axes");
  }
  {
     ::mlir::Builder odsBuilder(getContext());
     ::mlir::Attribute attr = getReductionAttr();
     if(attr && (attr == ::mlir::mesh::PartialAttr::get(odsBuilder.getContext(), ::mlir::mesh::Partial::Sum)))
       elidedAttrs.push_back("reduction");
  }
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), elidedAttrs);
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = getInput().getType();
    if (auto validType = ::llvm::dyn_cast<::mlir::TensorType>(type))
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
  _odsPrinter << ' ' << "->";
  _odsPrinter << ' ';
  {
    auto type = getResult().getType();
    if (auto validType = ::llvm::dyn_cast<::mlir::RankedTensorType>(type))
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

} // namespace mesh
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::mesh::ReduceScatterOp)

namespace mlir {
namespace mesh {

//===----------------------------------------------------------------------===//
// ::mlir::mesh::ShardOp definitions
//===----------------------------------------------------------------------===//

namespace detail {
ShardOpGenericAdaptorBase::ShardOpGenericAdaptorBase(::mlir::DictionaryAttr attrs, const Properties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), properties(properties), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("mesh.shard", odsAttrs.getContext());
}

ShardOpGenericAdaptorBase::ShardOpGenericAdaptorBase(ShardOp op) : ShardOpGenericAdaptorBase(op->getDiscardableAttrDictionary(), op.getProperties(), op->getRegions()) {}

std::pair<unsigned, unsigned> ShardOpGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr ShardOpGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

::mlir::mesh::MeshShardingAttr ShardOpGenericAdaptorBase::getShardAttr() {
  auto attr = ::llvm::cast<::mlir::mesh::MeshShardingAttr>(getProperties().shard);
  return attr;
}

::mlir::mesh::MeshShardingAttr ShardOpGenericAdaptorBase::getShard() {
  auto attr = getShardAttr();
  return ::llvm::cast<::mlir::mesh::MeshShardingAttr>(attr);
}

::mlir::UnitAttr ShardOpGenericAdaptorBase::getAnnotateForUsersAttr() {
  auto attr = ::llvm::dyn_cast_or_null<::mlir::UnitAttr>(getProperties().annotate_for_users);
  if (!attr)
    attr = ((false) ? ::mlir::Builder(odsAttrs.getContext()).getUnitAttr() : nullptr);
  return attr;
}

bool ShardOpGenericAdaptorBase::getAnnotateForUsers() {
  auto attr = getAnnotateForUsersAttr();
    if (!attr)
      return ((false) ? ::mlir::Builder(odsAttrs.getContext()).getUnitAttr() : nullptr) != nullptr;
  return attr != nullptr;
}

} // namespace detail
ShardOpAdaptor::ShardOpAdaptor(ShardOp op) : ShardOpGenericAdaptor(op->getOperands(), op) {}

::mlir::LogicalResult ShardOpAdaptor::verify(::mlir::Location loc) {
  auto tblgen_annotate_for_users = getProperties().annotate_for_users; (void)tblgen_annotate_for_users;
  auto tblgen_shard = getProperties().shard; (void)tblgen_shard;
  if (!tblgen_shard) return emitError(loc, "'mesh.shard' op ""requires attribute 'shard'");

  if (tblgen_shard && !((::llvm::isa<::mlir::mesh::MeshShardingAttr>(tblgen_shard))))
    return emitError(loc, "'mesh.shard' op ""attribute 'shard' failed to satisfy constraint: Attribute that extends tensor type to distributed tensor type.");

  if (tblgen_annotate_for_users && !((::llvm::isa<::mlir::UnitAttr>(tblgen_annotate_for_users))))
    return emitError(loc, "'mesh.shard' op ""attribute 'annotate_for_users' failed to satisfy constraint: unit attribute");
  return ::mlir::success();
}

std::pair<unsigned, unsigned> ShardOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range ShardOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::TypedValue<::mlir::RankedTensorType> ShardOp::getSrc() {
  return ::llvm::cast<::mlir::TypedValue<::mlir::RankedTensorType>>(*getODSOperands(0).begin());
}

::mlir::OpOperand &ShardOp::getSrcMutable() {
  auto range = getODSOperandIndexAndLength(0);
  return getOperation()->getOpOperand(range.first);
}

std::pair<unsigned, unsigned> ShardOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range ShardOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::TypedValue<::mlir::RankedTensorType> ShardOp::getResult() {
  return ::llvm::cast<::mlir::TypedValue<::mlir::RankedTensorType>>(*getODSResults(0).begin());
}

::mlir::LogicalResult ShardOp::setPropertiesFromAttr(Properties &prop, ::mlir::Attribute attr, ::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
  ::mlir::DictionaryAttr dict = ::llvm::dyn_cast<::mlir::DictionaryAttr>(attr);
  if (!dict) {
    emitError() << "expected DictionaryAttr to set properties";
    return ::mlir::failure();
  }

  {
    auto &propStorage = prop.annotate_for_users;
       auto attr = dict.get("annotate_for_users");
    if (attr || /*isRequired=*/false) {
      if (!attr) {
        emitError() << "expected key entry for annotate_for_users in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `annotate_for_users` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }

  {
    auto &propStorage = prop.shard;
       auto attr = dict.get("shard");
    if (attr || /*isRequired=*/true) {
      if (!attr) {
        emitError() << "expected key entry for shard in DictionaryAttr to set "
                   "Properties.";
        return ::mlir::failure();
      }
      auto convertedAttr = ::llvm::dyn_cast<std::remove_reference_t<decltype(propStorage)>>(attr);
      if (convertedAttr) {
        propStorage = convertedAttr;
      } else {
        emitError() << "Invalid attribute `shard` in property conversion: " << attr;
        return ::mlir::failure();
      }
    }
  }
  return ::mlir::success();
}

::mlir::Attribute ShardOp::getPropertiesAsAttr(::mlir::MLIRContext *ctx, const Properties &prop) {
    ::mlir::SmallVector<::mlir::NamedAttribute> attrs;
    ::mlir::Builder odsBuilder{ctx};

    {
      const auto &propStorage = prop.annotate_for_users;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("annotate_for_users",
                                       propStorage));
    }

    {
      const auto &propStorage = prop.shard;
      if (propStorage)
        attrs.push_back(odsBuilder.getNamedAttr("shard",
                                       propStorage));
    }

  if (!attrs.empty())
    return odsBuilder.getDictionaryAttr(attrs);
  return {};
}

llvm::hash_code ShardOp::computePropertiesHash(const Properties &prop) {
  return llvm::hash_combine(
    llvm::hash_value(prop.annotate_for_users.getAsOpaquePointer()), 
    llvm::hash_value(prop.shard.getAsOpaquePointer()));
}

std::optional<mlir::Attribute> ShardOp::getInherentAttr(::mlir::MLIRContext *ctx, const Properties &prop, llvm::StringRef name) {
    if (name == "annotate_for_users")
      return prop.annotate_for_users;

    if (name == "shard")
      return prop.shard;
  return std::nullopt;
}

void ShardOp::setInherentAttr(Properties &prop, llvm::StringRef name, mlir::Attribute value) {
    if (name == "annotate_for_users") {
       prop.annotate_for_users = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.annotate_for_users)>>(value);
       return;
    }

    if (name == "shard") {
       prop.shard = ::llvm::dyn_cast_or_null<std::remove_reference_t<decltype(prop.shard)>>(value);
       return;
    }
}

void ShardOp::populateInherentAttrs(::mlir::MLIRContext *ctx, const Properties &prop, ::mlir::NamedAttrList &attrs) {
    if (prop.annotate_for_users) attrs.append("annotate_for_users", prop.annotate_for_users);

    if (prop.shard) attrs.append("shard", prop.shard);
}

::mlir::LogicalResult ShardOp::verifyInherentAttrs(::mlir::OperationName opName, ::mlir::NamedAttrList &attrs, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) {
    {
      ::mlir::Attribute attr = attrs.get(getAnnotateForUsersAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps8(attr, "annotate_for_users", emitError)))
        return ::mlir::failure();
    }

    {
      ::mlir::Attribute attr = attrs.get(getShardAttrName(opName));
      if (attr && ::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps7(attr, "shard", emitError)))
        return ::mlir::failure();
    }
    return ::mlir::success();
}

::mlir::LogicalResult ShardOp::readProperties(::mlir::DialectBytecodeReader &reader, ::mlir::OperationState &state) {
  auto &prop = state.getOrAddProperties<Properties>(); (void)prop;
  if (::mlir::failed(reader.readOptionalAttribute(prop.annotate_for_users)))
    return ::mlir::failure();

  if (::mlir::failed(reader.readAttribute(prop.shard)))
    return ::mlir::failure();
  return ::mlir::success();
}

void ShardOp::writeProperties(::mlir::DialectBytecodeWriter &writer) {
  auto &prop = getProperties(); (void)prop;

  writer.writeOptionalAttribute(prop.annotate_for_users);
  writer.writeAttribute(prop.shard);
}

::mlir::mesh::MeshShardingAttr ShardOp::getShardAttr() {
  return ::llvm::cast<::mlir::mesh::MeshShardingAttr>(getProperties().shard);
}

::mlir::mesh::MeshShardingAttr ShardOp::getShard() {
  auto attr = getShardAttr();
  return ::llvm::cast<::mlir::mesh::MeshShardingAttr>(attr);
}

::mlir::UnitAttr ShardOp::getAnnotateForUsersAttr() {
  return ::llvm::dyn_cast_or_null<::mlir::UnitAttr>(getProperties().annotate_for_users);
}

bool ShardOp::getAnnotateForUsers() {
  auto attr = getAnnotateForUsersAttr();
    if (!attr)
      return ((false) ? ::mlir::Builder((*this)->getContext()).getUnitAttr() : nullptr) != nullptr;
  return attr != nullptr;
}

void ShardOp::setShardAttr(::mlir::mesh::MeshShardingAttr attr) {
  (*this)->setAttr(getShardAttrName(), attr);
}

void ShardOp::setAnnotateForUsersAttr(::mlir::UnitAttr attr) {
  (*this)->setAttr(getAnnotateForUsersAttrName(), attr);
}

void ShardOp::setAnnotateForUsers(bool attrValue) {
    if (attrValue)
      return (*this)->setAttr(getAnnotateForUsersAttrName(), ((attrValue) ? ::mlir::Builder((*this)->getContext()).getUnitAttr() : nullptr));
    (*this)->removeAttr(getAnnotateForUsersAttrName());
}

::mlir::Attribute ShardOp::removeAnnotateForUsersAttr() {
    auto &attr = getProperties().annotate_for_users;
    attr = {};
    return attr;
}

void ShardOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value src, ::mlir::mesh::MeshShardingAttr shard, /*optional*/::mlir::UnitAttr annotate_for_users) {
  odsState.addOperands(src);
  odsState.getOrAddProperties<Properties>().shard = shard;
  if (annotate_for_users) {
    odsState.getOrAddProperties<Properties>().annotate_for_users = annotate_for_users;
  }
  odsState.addTypes(result);
}

void ShardOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value src, ::mlir::mesh::MeshShardingAttr shard, /*optional*/::mlir::UnitAttr annotate_for_users) {
  odsState.addOperands(src);
  odsState.getOrAddProperties<Properties>().shard = shard;
  if (annotate_for_users) {
    odsState.getOrAddProperties<Properties>().annotate_for_users = annotate_for_users;
  }

        ::llvm::SmallVector<::mlir::Type, 2> inferredReturnTypes;
        if (::mlir::succeeded(ShardOp::inferReturnTypes(odsBuilder.getContext(),
                      odsState.location, odsState.operands,
                      odsState.attributes.getDictionary(odsState.getContext()),
                      odsState.getRawProperties(),
                      odsState.regions, inferredReturnTypes)))
          odsState.addTypes(inferredReturnTypes);
        else
          ::llvm::report_fatal_error("Failed to infer result type(s).");
}

void ShardOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value src, ::mlir::mesh::MeshShardingAttr shard, /*optional*/::mlir::UnitAttr annotate_for_users) {
  odsState.addOperands(src);
  odsState.getOrAddProperties<Properties>().shard = shard;
  if (annotate_for_users) {
    odsState.getOrAddProperties<Properties>().annotate_for_users = annotate_for_users;
  }
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void ShardOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value src, ::mlir::mesh::MeshShardingAttr shard, /*optional*/bool annotate_for_users) {
  odsState.addOperands(src);
  odsState.getOrAddProperties<Properties>().shard = shard;
  if (annotate_for_users) {
    odsState.getOrAddProperties<Properties>().annotate_for_users = ((annotate_for_users) ? odsBuilder.getUnitAttr() : nullptr);
  }
  odsState.addTypes(result);
}

void ShardOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value src, ::mlir::mesh::MeshShardingAttr shard, /*optional*/bool annotate_for_users) {
  odsState.addOperands(src);
  odsState.getOrAddProperties<Properties>().shard = shard;
  if (annotate_for_users) {
    odsState.getOrAddProperties<Properties>().annotate_for_users = ((annotate_for_users) ? odsBuilder.getUnitAttr() : nullptr);
  }

        ::llvm::SmallVector<::mlir::Type, 2> inferredReturnTypes;
        if (::mlir::succeeded(ShardOp::inferReturnTypes(odsBuilder.getContext(),
                      odsState.location, odsState.operands,
                      odsState.attributes.getDictionary(odsState.getContext()),
                      odsState.getRawProperties(),
                      odsState.regions, inferredReturnTypes)))
          odsState.addTypes(inferredReturnTypes);
        else
          ::llvm::report_fatal_error("Failed to infer result type(s).");
}

void ShardOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value src, ::mlir::mesh::MeshShardingAttr shard, /*optional*/bool annotate_for_users) {
  odsState.addOperands(src);
  odsState.getOrAddProperties<Properties>().shard = shard;
  if (annotate_for_users) {
    odsState.getOrAddProperties<Properties>().annotate_for_users = ((annotate_for_users) ? odsBuilder.getUnitAttr() : nullptr);
  }
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void ShardOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

void ShardOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);

  ::llvm::SmallVector<::mlir::Type, 2> inferredReturnTypes;
  if (::mlir::succeeded(ShardOp::inferReturnTypes(odsBuilder.getContext(),
          odsState.location, operands,
          odsState.attributes.getDictionary(odsState.getContext()),
          odsState.getRawProperties(),
          odsState.regions, inferredReturnTypes))) {
    assert(inferredReturnTypes.size() == 1u && "mismatched number of return types");
    odsState.addTypes(inferredReturnTypes);
  } else {
    ::llvm::report_fatal_error("Failed to infer result type(s).");
  }
}

::mlir::LogicalResult ShardOp::verifyInvariantsImpl() {
  auto tblgen_annotate_for_users = getProperties().annotate_for_users; (void)tblgen_annotate_for_users;
  auto tblgen_shard = getProperties().shard; (void)tblgen_shard;
  if (!tblgen_shard) return emitOpError("requires attribute 'shard'");

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps7(*this, tblgen_shard, "shard")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_MeshOps8(*this, tblgen_annotate_for_users, "annotate_for_users")))
    return ::mlir::failure();
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_MeshOps2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_MeshOps2(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult ShardOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

::mlir::LogicalResult ShardOp::inferReturnTypes(::mlir::MLIRContext *context, ::std::optional<::mlir::Location> location, ::mlir::ValueRange operands, ::mlir::DictionaryAttr attributes, ::mlir::OpaqueProperties properties, ::mlir::RegionRange regions, ::llvm::SmallVectorImpl<::mlir::Type>&inferredReturnTypes) {
  inferredReturnTypes.resize(1);
  ::mlir::Builder odsBuilder(context);
  ::mlir::Type odsInferredType0 = operands[0].getType();
  inferredReturnTypes[0] = odsInferredType0;
  return ::mlir::success();
}

::mlir::ParseResult ShardOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::UnresolvedOperand srcRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::UnresolvedOperand> srcOperands(srcRawOperands);  ::llvm::SMLoc srcOperandsLoc;
  (void)srcOperandsLoc;
  ::mlir::mesh::MeshShardingAttr shardAttr;
  ::mlir::Type resultRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> resultTypes(resultRawTypes);

  srcOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(srcRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseKeyword("to"))
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(shardAttr, ::mlir::Type{})) {
    return ::mlir::failure();
  }
  if (shardAttr) result.getOrAddProperties<ShardOp::Properties>().shard = shardAttr;
  if (::mlir::succeeded(parser.parseOptionalKeyword("annotate_for_users"))) {
    result.getOrAddProperties<ShardOp::Properties>().annotate_for_users = parser.getBuilder().getUnitAttr();  }
  {
    auto loc = parser.getCurrentLocation();(void)loc;
    if (parser.parseOptionalAttrDict(result.attributes))
      return ::mlir::failure();
    if (failed(verifyInherentAttrs(result.name, result.attributes, [&]() {
        return parser.emitError(loc) << "'" << result.name.getStringRef() << "' op ";
      })))
      return ::mlir::failure();
  }
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::RankedTensorType type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    resultRawTypes[0] = type;
  }
  result.addTypes(resultTypes);
  if (parser.resolveOperands(srcOperands, resultTypes[0], srcOperandsLoc, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void ShardOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  _odsPrinter << getSrc();
  _odsPrinter << ' ' << "to";
  _odsPrinter << ' ';
_odsPrinter.printStrippedAttrOrType(getShardAttr());
  if (getAnnotateForUsersAttr()) {
    _odsPrinter << ' ' << "annotate_for_users";
  }
  ::llvm::SmallVector<::llvm::StringRef, 2> elidedAttrs;
  elidedAttrs.push_back("shard");
  elidedAttrs.push_back("annotate_for_users");
  {
     ::mlir::Builder odsBuilder(getContext());
     ::mlir::Attribute attr = getAnnotateForUsersAttr();
     if(attr && (attr == ((false) ? odsBuilder.getUnitAttr() : nullptr)))
       elidedAttrs.push_back("annotate_for_users");
  }
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), elidedAttrs);
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = getResult().getType();
    if (auto validType = ::llvm::dyn_cast<::mlir::RankedTensorType>(type))
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

void ShardOp::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
}

} // namespace mesh
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::mesh::ShardOp)


#endif  // GET_OP_CLASSES

