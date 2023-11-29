/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Declarations                                                            *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|* From: MeshOps.td                                                           *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#if defined(GET_OP_CLASSES) || defined(GET_OP_FWD_DEFINES)
#undef GET_OP_FWD_DEFINES
namespace mlir {
namespace mesh {
class AllGatherOp;
} // namespace mesh
} // namespace mlir
namespace mlir {
namespace mesh {
class AllReduceOp;
} // namespace mesh
} // namespace mlir
namespace mlir {
namespace mesh {
class AllToAllOp;
} // namespace mesh
} // namespace mlir
namespace mlir {
namespace mesh {
class ClusterOp;
} // namespace mesh
} // namespace mlir
namespace mlir {
namespace mesh {
class ReduceScatterOp;
} // namespace mesh
} // namespace mlir
namespace mlir {
namespace mesh {
class ShardOp;
} // namespace mesh
} // namespace mlir
#endif

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace mesh {

//===----------------------------------------------------------------------===//
// ::mlir::mesh::AllGatherOp declarations
//===----------------------------------------------------------------------===//

namespace detail {
class AllGatherOpGenericAdaptorBase {
public:
  struct Properties {
    using gather_axisTy = ::mlir::IntegerAttr;
    gather_axisTy gather_axis;

    auto getGatherAxis() {
      auto &propStorage = this->gather_axis;
      return ::llvm::cast<::mlir::IntegerAttr>(propStorage);
    }
    void setGatherAxis(const ::mlir::IntegerAttr &propValue) {
      this->gather_axis = propValue;
    }
    using meshTy = ::mlir::FlatSymbolRefAttr;
    meshTy mesh;

    auto getMesh() {
      auto &propStorage = this->mesh;
      return ::llvm::cast<::mlir::FlatSymbolRefAttr>(propStorage);
    }
    void setMesh(const ::mlir::FlatSymbolRefAttr &propValue) {
      this->mesh = propValue;
    }
    using mesh_axesTy = ::mlir::DenseI16ArrayAttr;
    mesh_axesTy mesh_axes;

    auto getMeshAxes() {
      auto &propStorage = this->mesh_axes;
      return ::llvm::dyn_cast_or_null<::mlir::DenseI16ArrayAttr>(propStorage);
    }
    void setMeshAxes(const ::mlir::DenseI16ArrayAttr &propValue) {
      this->mesh_axes = propValue;
    }
    bool operator==(const Properties &rhs) const {
      return 
        rhs.gather_axis == this->gather_axis &&
        rhs.mesh == this->mesh &&
        rhs.mesh_axes == this->mesh_axes &&
        true;
    }
    bool operator!=(const Properties &rhs) const {
      return !(*this == rhs);
    }
  };
protected:
  ::mlir::DictionaryAttr odsAttrs;
  ::std::optional<::mlir::OperationName> odsOpName;
  Properties properties;
  ::mlir::RegionRange odsRegions;
public:
  AllGatherOpGenericAdaptorBase(::mlir::DictionaryAttr attrs = nullptr, const Properties &properties = {}, ::mlir::RegionRange regions = {});

  AllGatherOpGenericAdaptorBase(AllGatherOp op);

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize);
  const Properties &getProperties() {
    return properties;
  }

  ::mlir::DictionaryAttr getAttributes();
  ::mlir::FlatSymbolRefAttr getMeshAttr();
  ::llvm::StringRef getMesh();
  ::mlir::DenseI16ArrayAttr getMeshAxesAttr();
  ::llvm::ArrayRef<int16_t> getMeshAxes();
  ::mlir::IntegerAttr getGatherAxisAttr();
  ::llvm::APInt getGatherAxis();
};
} // namespace detail
template <typename RangeT>
class AllGatherOpGenericAdaptor : public detail::AllGatherOpGenericAdaptorBase {
  using ValueT = ::llvm::detail::ValueOfRange<RangeT>;
  using Base = detail::AllGatherOpGenericAdaptorBase;
public:
  AllGatherOpGenericAdaptor(RangeT values, ::mlir::DictionaryAttr attrs = nullptr, const Properties &properties = {}, ::mlir::RegionRange regions = {}) : Base(attrs, properties, regions), odsOperands(values) {}

  AllGatherOpGenericAdaptor(RangeT values, ::mlir::DictionaryAttr attrs, ::mlir::OpaqueProperties properties, ::mlir::RegionRange regions = {}) : AllGatherOpGenericAdaptor(values, attrs, (properties ? *properties.as<Properties *>() : Properties{}), regions) {}

  template <typename LateInst = AllGatherOp, typename = std::enable_if_t<std::is_same_v<LateInst, AllGatherOp>>>
  AllGatherOpGenericAdaptor(RangeT values, LateInst op) : Base(op), odsOperands(values) {}

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index) {
    return Base::getODSOperandIndexAndLength(index, odsOperands.size());
  }

  RangeT getODSOperands(unsigned index) {
    auto valueRange = getODSOperandIndexAndLength(index);
    return {std::next(odsOperands.begin(), valueRange.first),
             std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
  }

  ValueT getInput() {
    return (*getODSOperands(0).begin());
  }

  RangeT getOperands() {
    return odsOperands;
  }

private:
  RangeT odsOperands;
};
class AllGatherOpAdaptor : public AllGatherOpGenericAdaptor<::mlir::ValueRange> {
public:
  using AllGatherOpGenericAdaptor::AllGatherOpGenericAdaptor;
  AllGatherOpAdaptor(AllGatherOp op);

  ::mlir::LogicalResult verify(::mlir::Location loc);
};
class AllGatherOp : public ::mlir::Op<AllGatherOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::TensorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::OpInvariants, ::mlir::BytecodeOpInterface::Trait, ::mlir::OpTrait::SameOperandsAndResultElementType, ::mlir::OpTrait::SameOperandsAndResultRank, ::mlir::SymbolUserOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = AllGatherOpAdaptor;
  template <typename RangeT>
  using GenericAdaptor = AllGatherOpGenericAdaptor<RangeT>;
  using FoldAdaptor = GenericAdaptor<::llvm::ArrayRef<::mlir::Attribute>>;
  using Properties = FoldAdaptor::Properties;
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("gather_axis"), ::llvm::StringRef("mesh"), ::llvm::StringRef("mesh_axes")};
    return ::llvm::ArrayRef(attrNames);
  }

  ::mlir::StringAttr getGatherAxisAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getGatherAxisAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getMeshAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getMeshAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getMeshAxesAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getMeshAxesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("mesh.all_gather");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getInput();
  ::mlir::OpOperand &getInputMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getResult();
  static ::mlir::LogicalResult setPropertiesFromAttr(Properties &prop, ::mlir::Attribute attr, ::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError);
  static ::mlir::Attribute getPropertiesAsAttr(::mlir::MLIRContext *ctx, const Properties &prop);
  static llvm::hash_code computePropertiesHash(const Properties &prop);
  static std::optional<mlir::Attribute> getInherentAttr(::mlir::MLIRContext *ctx, const Properties &prop, llvm::StringRef name);
  static void setInherentAttr(Properties &prop, llvm::StringRef name, mlir::Attribute value);
  static void populateInherentAttrs(::mlir::MLIRContext *ctx, const Properties &prop, ::mlir::NamedAttrList &attrs);
  static ::mlir::LogicalResult verifyInherentAttrs(::mlir::OperationName opName, ::mlir::NamedAttrList &attrs, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError);
  static ::mlir::LogicalResult readProperties(::mlir::DialectBytecodeReader &reader, ::mlir::OperationState &state);
  void writeProperties(::mlir::DialectBytecodeWriter &writer);
  ::mlir::FlatSymbolRefAttr getMeshAttr();
  ::llvm::StringRef getMesh();
  ::mlir::DenseI16ArrayAttr getMeshAxesAttr();
  ::llvm::ArrayRef<int16_t> getMeshAxes();
  ::mlir::IntegerAttr getGatherAxisAttr();
  ::llvm::APInt getGatherAxis();
  void setMeshAttr(::mlir::FlatSymbolRefAttr attr);
  void setMesh(::llvm::StringRef attrValue);
  void setMeshAxesAttr(::mlir::DenseI16ArrayAttr attr);
  void setMeshAxes(::llvm::ArrayRef<int16_t> attrValue);
  void setGatherAxisAttr(::mlir::IntegerAttr attr);
  void setGatherAxis(::llvm::APInt attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::IntegerAttr gather_axis);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::IntegerAttr gather_axis);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::llvm::APInt gather_axis);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::llvm::APInt gather_axis);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static void populateDefaultProperties(::mlir::OperationName opName, Properties &properties);
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  static void getCanonicalizationPatterns(::mlir::RewritePatternSet &results, ::mlir::MLIRContext *context);
  ::mlir::LogicalResult verifySymbolUses(::mlir::SymbolTableCollection &symbolTable);
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 3 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    assert(name.isRegistered() && "Operation isn't registered, missing a "
          "dependent dialect loading?");
    return name.getAttributeNames()[index];
  }

public:
};
} // namespace mesh
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::mesh::AllGatherOp)

namespace mlir {
namespace mesh {

//===----------------------------------------------------------------------===//
// ::mlir::mesh::AllReduceOp declarations
//===----------------------------------------------------------------------===//

namespace detail {
class AllReduceOpGenericAdaptorBase {
public:
  struct Properties {
    using meshTy = ::mlir::FlatSymbolRefAttr;
    meshTy mesh;

    auto getMesh() {
      auto &propStorage = this->mesh;
      return ::llvm::cast<::mlir::FlatSymbolRefAttr>(propStorage);
    }
    void setMesh(const ::mlir::FlatSymbolRefAttr &propValue) {
      this->mesh = propValue;
    }
    using mesh_axesTy = ::mlir::DenseI16ArrayAttr;
    mesh_axesTy mesh_axes;

    auto getMeshAxes() {
      auto &propStorage = this->mesh_axes;
      return ::llvm::dyn_cast_or_null<::mlir::DenseI16ArrayAttr>(propStorage);
    }
    void setMeshAxes(const ::mlir::DenseI16ArrayAttr &propValue) {
      this->mesh_axes = propValue;
    }
    using reductionTy = ::mlir::mesh::PartialAttr;
    reductionTy reduction;

    auto getReduction() {
      auto &propStorage = this->reduction;
      return ::llvm::dyn_cast_or_null<::mlir::mesh::PartialAttr>(propStorage);
    }
    void setReduction(const ::mlir::mesh::PartialAttr &propValue) {
      this->reduction = propValue;
    }
    bool operator==(const Properties &rhs) const {
      return 
        rhs.mesh == this->mesh &&
        rhs.mesh_axes == this->mesh_axes &&
        rhs.reduction == this->reduction &&
        true;
    }
    bool operator!=(const Properties &rhs) const {
      return !(*this == rhs);
    }
  };
protected:
  ::mlir::DictionaryAttr odsAttrs;
  ::std::optional<::mlir::OperationName> odsOpName;
  Properties properties;
  ::mlir::RegionRange odsRegions;
public:
  AllReduceOpGenericAdaptorBase(::mlir::DictionaryAttr attrs = nullptr, const Properties &properties = {}, ::mlir::RegionRange regions = {});

  AllReduceOpGenericAdaptorBase(AllReduceOp op);

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize);
  const Properties &getProperties() {
    return properties;
  }

  ::mlir::DictionaryAttr getAttributes();
  ::mlir::FlatSymbolRefAttr getMeshAttr();
  ::llvm::StringRef getMesh();
  ::mlir::DenseI16ArrayAttr getMeshAxesAttr();
  ::llvm::ArrayRef<int16_t> getMeshAxes();
  ::mlir::mesh::PartialAttr getReductionAttr();
  ::mlir::mesh::Partial getReduction();
};
} // namespace detail
template <typename RangeT>
class AllReduceOpGenericAdaptor : public detail::AllReduceOpGenericAdaptorBase {
  using ValueT = ::llvm::detail::ValueOfRange<RangeT>;
  using Base = detail::AllReduceOpGenericAdaptorBase;
public:
  AllReduceOpGenericAdaptor(RangeT values, ::mlir::DictionaryAttr attrs = nullptr, const Properties &properties = {}, ::mlir::RegionRange regions = {}) : Base(attrs, properties, regions), odsOperands(values) {}

  AllReduceOpGenericAdaptor(RangeT values, ::mlir::DictionaryAttr attrs, ::mlir::OpaqueProperties properties, ::mlir::RegionRange regions = {}) : AllReduceOpGenericAdaptor(values, attrs, (properties ? *properties.as<Properties *>() : Properties{}), regions) {}

  template <typename LateInst = AllReduceOp, typename = std::enable_if_t<std::is_same_v<LateInst, AllReduceOp>>>
  AllReduceOpGenericAdaptor(RangeT values, LateInst op) : Base(op), odsOperands(values) {}

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index) {
    return Base::getODSOperandIndexAndLength(index, odsOperands.size());
  }

  RangeT getODSOperands(unsigned index) {
    auto valueRange = getODSOperandIndexAndLength(index);
    return {std::next(odsOperands.begin(), valueRange.first),
             std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
  }

  ValueT getInput() {
    return (*getODSOperands(0).begin());
  }

  RangeT getOperands() {
    return odsOperands;
  }

private:
  RangeT odsOperands;
};
class AllReduceOpAdaptor : public AllReduceOpGenericAdaptor<::mlir::ValueRange> {
public:
  using AllReduceOpGenericAdaptor::AllReduceOpGenericAdaptor;
  AllReduceOpAdaptor(AllReduceOp op);

  ::mlir::LogicalResult verify(::mlir::Location loc);
};
class AllReduceOp : public ::mlir::Op<AllReduceOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::RankedTensorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::OpInvariants, ::mlir::BytecodeOpInterface::Trait, ::mlir::OpTrait::SameOperandsAndResultShape, ::mlir::SymbolUserOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = AllReduceOpAdaptor;
  template <typename RangeT>
  using GenericAdaptor = AllReduceOpGenericAdaptor<RangeT>;
  using FoldAdaptor = GenericAdaptor<::llvm::ArrayRef<::mlir::Attribute>>;
  using Properties = FoldAdaptor::Properties;
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("mesh"), ::llvm::StringRef("mesh_axes"), ::llvm::StringRef("reduction")};
    return ::llvm::ArrayRef(attrNames);
  }

  ::mlir::StringAttr getMeshAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getMeshAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getMeshAxesAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getMeshAxesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getReductionAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getReductionAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("mesh.all_reduce");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::RankedTensorType> getInput();
  ::mlir::OpOperand &getInputMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::RankedTensorType> getResult();
  static ::mlir::LogicalResult setPropertiesFromAttr(Properties &prop, ::mlir::Attribute attr, ::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError);
  static ::mlir::Attribute getPropertiesAsAttr(::mlir::MLIRContext *ctx, const Properties &prop);
  static llvm::hash_code computePropertiesHash(const Properties &prop);
  static std::optional<mlir::Attribute> getInherentAttr(::mlir::MLIRContext *ctx, const Properties &prop, llvm::StringRef name);
  static void setInherentAttr(Properties &prop, llvm::StringRef name, mlir::Attribute value);
  static void populateInherentAttrs(::mlir::MLIRContext *ctx, const Properties &prop, ::mlir::NamedAttrList &attrs);
  static ::mlir::LogicalResult verifyInherentAttrs(::mlir::OperationName opName, ::mlir::NamedAttrList &attrs, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError);
  static ::mlir::LogicalResult readProperties(::mlir::DialectBytecodeReader &reader, ::mlir::OperationState &state);
  void writeProperties(::mlir::DialectBytecodeWriter &writer);
  ::mlir::FlatSymbolRefAttr getMeshAttr();
  ::llvm::StringRef getMesh();
  ::mlir::DenseI16ArrayAttr getMeshAxesAttr();
  ::llvm::ArrayRef<int16_t> getMeshAxes();
  ::mlir::mesh::PartialAttr getReductionAttr();
  ::mlir::mesh::Partial getReduction();
  void setMeshAttr(::mlir::FlatSymbolRefAttr attr);
  void setMesh(::llvm::StringRef attrValue);
  void setMeshAxesAttr(::mlir::DenseI16ArrayAttr attr);
  void setMeshAxes(::llvm::ArrayRef<int16_t> attrValue);
  void setReductionAttr(::mlir::mesh::PartialAttr attr);
  void setReduction(::mlir::mesh::Partial attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::mesh::PartialAttr reduction);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::mesh::PartialAttr reduction);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::mlir::mesh::Partial reduction = ::mlir::mesh::Partial::Sum);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::mlir::mesh::Partial reduction = ::mlir::mesh::Partial::Sum);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static void populateDefaultProperties(::mlir::OperationName opName, Properties &properties);
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  static void getCanonicalizationPatterns(::mlir::RewritePatternSet &results, ::mlir::MLIRContext *context);
  ::mlir::LogicalResult verifySymbolUses(::mlir::SymbolTableCollection &symbolTable);
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 3 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    assert(name.isRegistered() && "Operation isn't registered, missing a "
          "dependent dialect loading?");
    return name.getAttributeNames()[index];
  }

public:
};
} // namespace mesh
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::mesh::AllReduceOp)

namespace mlir {
namespace mesh {

//===----------------------------------------------------------------------===//
// ::mlir::mesh::AllToAllOp declarations
//===----------------------------------------------------------------------===//

namespace detail {
class AllToAllOpGenericAdaptorBase {
public:
  struct Properties {
    using concat_axisTy = ::mlir::IntegerAttr;
    concat_axisTy concat_axis;

    auto getConcatAxis() {
      auto &propStorage = this->concat_axis;
      return ::llvm::cast<::mlir::IntegerAttr>(propStorage);
    }
    void setConcatAxis(const ::mlir::IntegerAttr &propValue) {
      this->concat_axis = propValue;
    }
    using meshTy = ::mlir::FlatSymbolRefAttr;
    meshTy mesh;

    auto getMesh() {
      auto &propStorage = this->mesh;
      return ::llvm::cast<::mlir::FlatSymbolRefAttr>(propStorage);
    }
    void setMesh(const ::mlir::FlatSymbolRefAttr &propValue) {
      this->mesh = propValue;
    }
    using mesh_axesTy = ::mlir::DenseI16ArrayAttr;
    mesh_axesTy mesh_axes;

    auto getMeshAxes() {
      auto &propStorage = this->mesh_axes;
      return ::llvm::dyn_cast_or_null<::mlir::DenseI16ArrayAttr>(propStorage);
    }
    void setMeshAxes(const ::mlir::DenseI16ArrayAttr &propValue) {
      this->mesh_axes = propValue;
    }
    using split_axisTy = ::mlir::IntegerAttr;
    split_axisTy split_axis;

    auto getSplitAxis() {
      auto &propStorage = this->split_axis;
      return ::llvm::cast<::mlir::IntegerAttr>(propStorage);
    }
    void setSplitAxis(const ::mlir::IntegerAttr &propValue) {
      this->split_axis = propValue;
    }
    bool operator==(const Properties &rhs) const {
      return 
        rhs.concat_axis == this->concat_axis &&
        rhs.mesh == this->mesh &&
        rhs.mesh_axes == this->mesh_axes &&
        rhs.split_axis == this->split_axis &&
        true;
    }
    bool operator!=(const Properties &rhs) const {
      return !(*this == rhs);
    }
  };
protected:
  ::mlir::DictionaryAttr odsAttrs;
  ::std::optional<::mlir::OperationName> odsOpName;
  Properties properties;
  ::mlir::RegionRange odsRegions;
public:
  AllToAllOpGenericAdaptorBase(::mlir::DictionaryAttr attrs = nullptr, const Properties &properties = {}, ::mlir::RegionRange regions = {});

  AllToAllOpGenericAdaptorBase(AllToAllOp op);

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize);
  const Properties &getProperties() {
    return properties;
  }

  ::mlir::DictionaryAttr getAttributes();
  ::mlir::FlatSymbolRefAttr getMeshAttr();
  ::llvm::StringRef getMesh();
  ::mlir::DenseI16ArrayAttr getMeshAxesAttr();
  ::llvm::ArrayRef<int16_t> getMeshAxes();
  ::mlir::IntegerAttr getSplitAxisAttr();
  ::llvm::APInt getSplitAxis();
  ::mlir::IntegerAttr getConcatAxisAttr();
  ::llvm::APInt getConcatAxis();
};
} // namespace detail
template <typename RangeT>
class AllToAllOpGenericAdaptor : public detail::AllToAllOpGenericAdaptorBase {
  using ValueT = ::llvm::detail::ValueOfRange<RangeT>;
  using Base = detail::AllToAllOpGenericAdaptorBase;
public:
  AllToAllOpGenericAdaptor(RangeT values, ::mlir::DictionaryAttr attrs = nullptr, const Properties &properties = {}, ::mlir::RegionRange regions = {}) : Base(attrs, properties, regions), odsOperands(values) {}

  AllToAllOpGenericAdaptor(RangeT values, ::mlir::DictionaryAttr attrs, ::mlir::OpaqueProperties properties, ::mlir::RegionRange regions = {}) : AllToAllOpGenericAdaptor(values, attrs, (properties ? *properties.as<Properties *>() : Properties{}), regions) {}

  template <typename LateInst = AllToAllOp, typename = std::enable_if_t<std::is_same_v<LateInst, AllToAllOp>>>
  AllToAllOpGenericAdaptor(RangeT values, LateInst op) : Base(op), odsOperands(values) {}

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index) {
    return Base::getODSOperandIndexAndLength(index, odsOperands.size());
  }

  RangeT getODSOperands(unsigned index) {
    auto valueRange = getODSOperandIndexAndLength(index);
    return {std::next(odsOperands.begin(), valueRange.first),
             std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
  }

  ValueT getInput() {
    return (*getODSOperands(0).begin());
  }

  RangeT getOperands() {
    return odsOperands;
  }

private:
  RangeT odsOperands;
};
class AllToAllOpAdaptor : public AllToAllOpGenericAdaptor<::mlir::ValueRange> {
public:
  using AllToAllOpGenericAdaptor::AllToAllOpGenericAdaptor;
  AllToAllOpAdaptor(AllToAllOp op);

  ::mlir::LogicalResult verify(::mlir::Location loc);
};
class AllToAllOp : public ::mlir::Op<AllToAllOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::TensorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::OpInvariants, ::mlir::BytecodeOpInterface::Trait, ::mlir::OpTrait::SameOperandsAndResultElementType, ::mlir::OpTrait::SameOperandsAndResultRank, ::mlir::SymbolUserOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = AllToAllOpAdaptor;
  template <typename RangeT>
  using GenericAdaptor = AllToAllOpGenericAdaptor<RangeT>;
  using FoldAdaptor = GenericAdaptor<::llvm::ArrayRef<::mlir::Attribute>>;
  using Properties = FoldAdaptor::Properties;
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("concat_axis"), ::llvm::StringRef("mesh"), ::llvm::StringRef("mesh_axes"), ::llvm::StringRef("split_axis")};
    return ::llvm::ArrayRef(attrNames);
  }

  ::mlir::StringAttr getConcatAxisAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getConcatAxisAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getMeshAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getMeshAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getMeshAxesAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getMeshAxesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr getSplitAxisAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getSplitAxisAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("mesh.all_to_all");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getInput();
  ::mlir::OpOperand &getInputMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getResult();
  static ::mlir::LogicalResult setPropertiesFromAttr(Properties &prop, ::mlir::Attribute attr, ::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError);
  static ::mlir::Attribute getPropertiesAsAttr(::mlir::MLIRContext *ctx, const Properties &prop);
  static llvm::hash_code computePropertiesHash(const Properties &prop);
  static std::optional<mlir::Attribute> getInherentAttr(::mlir::MLIRContext *ctx, const Properties &prop, llvm::StringRef name);
  static void setInherentAttr(Properties &prop, llvm::StringRef name, mlir::Attribute value);
  static void populateInherentAttrs(::mlir::MLIRContext *ctx, const Properties &prop, ::mlir::NamedAttrList &attrs);
  static ::mlir::LogicalResult verifyInherentAttrs(::mlir::OperationName opName, ::mlir::NamedAttrList &attrs, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError);
  static ::mlir::LogicalResult readProperties(::mlir::DialectBytecodeReader &reader, ::mlir::OperationState &state);
  void writeProperties(::mlir::DialectBytecodeWriter &writer);
  ::mlir::FlatSymbolRefAttr getMeshAttr();
  ::llvm::StringRef getMesh();
  ::mlir::DenseI16ArrayAttr getMeshAxesAttr();
  ::llvm::ArrayRef<int16_t> getMeshAxes();
  ::mlir::IntegerAttr getSplitAxisAttr();
  ::llvm::APInt getSplitAxis();
  ::mlir::IntegerAttr getConcatAxisAttr();
  ::llvm::APInt getConcatAxis();
  void setMeshAttr(::mlir::FlatSymbolRefAttr attr);
  void setMesh(::llvm::StringRef attrValue);
  void setMeshAxesAttr(::mlir::DenseI16ArrayAttr attr);
  void setMeshAxes(::llvm::ArrayRef<int16_t> attrValue);
  void setSplitAxisAttr(::mlir::IntegerAttr attr);
  void setSplitAxis(::llvm::APInt attrValue);
  void setConcatAxisAttr(::mlir::IntegerAttr attr);
  void setConcatAxis(::llvm::APInt attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::IntegerAttr split_axis, ::mlir::IntegerAttr concat_axis);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::IntegerAttr split_axis, ::mlir::IntegerAttr concat_axis);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::llvm::APInt split_axis, ::llvm::APInt concat_axis);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::llvm::APInt split_axis, ::llvm::APInt concat_axis);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static void populateDefaultProperties(::mlir::OperationName opName, Properties &properties);
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  static void getCanonicalizationPatterns(::mlir::RewritePatternSet &results, ::mlir::MLIRContext *context);
  ::mlir::LogicalResult verifySymbolUses(::mlir::SymbolTableCollection &symbolTable);
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 4 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    assert(name.isRegistered() && "Operation isn't registered, missing a "
          "dependent dialect loading?");
    return name.getAttributeNames()[index];
  }

public:
};
} // namespace mesh
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::mesh::AllToAllOp)

namespace mlir {
namespace mesh {

//===----------------------------------------------------------------------===//
// ::mlir::mesh::ClusterOp declarations
//===----------------------------------------------------------------------===//

namespace detail {
class ClusterOpGenericAdaptorBase {
public:
  struct Properties {
    using dim_sizesTy = ::mlir::DenseI64ArrayAttr;
    dim_sizesTy dim_sizes;

    auto getDimSizes() {
      auto &propStorage = this->dim_sizes;
      return ::llvm::dyn_cast_or_null<::mlir::DenseI64ArrayAttr>(propStorage);
    }
    void setDimSizes(const ::mlir::DenseI64ArrayAttr &propValue) {
      this->dim_sizes = propValue;
    }
    using rankTy = ::mlir::IntegerAttr;
    rankTy rank;

    auto getRank() {
      auto &propStorage = this->rank;
      return ::llvm::cast<::mlir::IntegerAttr>(propStorage);
    }
    void setRank(const ::mlir::IntegerAttr &propValue) {
      this->rank = propValue;
    }
    using sym_nameTy = ::mlir::StringAttr;
    sym_nameTy sym_name;

    auto getSymName() {
      auto &propStorage = this->sym_name;
      return ::llvm::cast<::mlir::StringAttr>(propStorage);
    }
    void setSymName(const ::mlir::StringAttr &propValue) {
      this->sym_name = propValue;
    }
    bool operator==(const Properties &rhs) const {
      return 
        rhs.dim_sizes == this->dim_sizes &&
        rhs.rank == this->rank &&
        rhs.sym_name == this->sym_name &&
        true;
    }
    bool operator!=(const Properties &rhs) const {
      return !(*this == rhs);
    }
  };
protected:
  ::mlir::DictionaryAttr odsAttrs;
  ::std::optional<::mlir::OperationName> odsOpName;
  Properties properties;
  ::mlir::RegionRange odsRegions;
public:
  ClusterOpGenericAdaptorBase(::mlir::DictionaryAttr attrs = nullptr, const Properties &properties = {}, ::mlir::RegionRange regions = {});

  ClusterOpGenericAdaptorBase(ClusterOp op);

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize);
  const Properties &getProperties() {
    return properties;
  }

  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getSymNameAttr();
  ::llvm::StringRef getSymName();
  ::mlir::IntegerAttr getRankAttr();
  uint64_t getRank();
  ::mlir::DenseI64ArrayAttr getDimSizesAttr();
  ::llvm::ArrayRef<int64_t> getDimSizes();
};
} // namespace detail
template <typename RangeT>
class ClusterOpGenericAdaptor : public detail::ClusterOpGenericAdaptorBase {
  using ValueT = ::llvm::detail::ValueOfRange<RangeT>;
  using Base = detail::ClusterOpGenericAdaptorBase;
public:
  ClusterOpGenericAdaptor(RangeT values, ::mlir::DictionaryAttr attrs = nullptr, const Properties &properties = {}, ::mlir::RegionRange regions = {}) : Base(attrs, properties, regions), odsOperands(values) {}

  ClusterOpGenericAdaptor(RangeT values, ::mlir::DictionaryAttr attrs, ::mlir::OpaqueProperties properties, ::mlir::RegionRange regions = {}) : ClusterOpGenericAdaptor(values, attrs, (properties ? *properties.as<Properties *>() : Properties{}), regions) {}

  template <typename LateInst = ClusterOp, typename = std::enable_if_t<std::is_same_v<LateInst, ClusterOp>>>
  ClusterOpGenericAdaptor(RangeT values, LateInst op) : Base(op), odsOperands(values) {}

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index) {
    return Base::getODSOperandIndexAndLength(index, odsOperands.size());
  }

  RangeT getODSOperands(unsigned index) {
    auto valueRange = getODSOperandIndexAndLength(index);
    return {std::next(odsOperands.begin(), valueRange.first),
             std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
  }

  RangeT getOperands() {
    return odsOperands;
  }

private:
  RangeT odsOperands;
};
class ClusterOpAdaptor : public ClusterOpGenericAdaptor<::mlir::ValueRange> {
public:
  using ClusterOpGenericAdaptor::ClusterOpGenericAdaptor;
  ClusterOpAdaptor(ClusterOp op);

  ::mlir::LogicalResult verify(::mlir::Location loc);
};
class ClusterOp : public ::mlir::Op<ClusterOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::ZeroOperands, ::mlir::OpTrait::OpInvariants, ::mlir::BytecodeOpInterface::Trait, ::mlir::SymbolOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = ClusterOpAdaptor;
  template <typename RangeT>
  using GenericAdaptor = ClusterOpGenericAdaptor<RangeT>;
  using FoldAdaptor = GenericAdaptor<::llvm::ArrayRef<::mlir::Attribute>>;
  using Properties = FoldAdaptor::Properties;
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("dim_sizes"), ::llvm::StringRef("rank"), ::llvm::StringRef("sym_name")};
    return ::llvm::ArrayRef(attrNames);
  }

  ::mlir::StringAttr getDimSizesAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getDimSizesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getRankAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getRankAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getSymNameAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getSymNameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("mesh.cluster");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  static ::mlir::LogicalResult setPropertiesFromAttr(Properties &prop, ::mlir::Attribute attr, ::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError);
  static ::mlir::Attribute getPropertiesAsAttr(::mlir::MLIRContext *ctx, const Properties &prop);
  static llvm::hash_code computePropertiesHash(const Properties &prop);
  static std::optional<mlir::Attribute> getInherentAttr(::mlir::MLIRContext *ctx, const Properties &prop, llvm::StringRef name);
  static void setInherentAttr(Properties &prop, llvm::StringRef name, mlir::Attribute value);
  static void populateInherentAttrs(::mlir::MLIRContext *ctx, const Properties &prop, ::mlir::NamedAttrList &attrs);
  static ::mlir::LogicalResult verifyInherentAttrs(::mlir::OperationName opName, ::mlir::NamedAttrList &attrs, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError);
  static ::mlir::LogicalResult readProperties(::mlir::DialectBytecodeReader &reader, ::mlir::OperationState &state);
  void writeProperties(::mlir::DialectBytecodeWriter &writer);
  ::mlir::StringAttr getSymNameAttr();
  ::llvm::StringRef getSymName();
  ::mlir::IntegerAttr getRankAttr();
  uint64_t getRank();
  ::mlir::DenseI64ArrayAttr getDimSizesAttr();
  ::llvm::ArrayRef<int64_t> getDimSizes();
  void setSymNameAttr(::mlir::StringAttr attr);
  void setSymName(::llvm::StringRef attrValue);
  void setRankAttr(::mlir::IntegerAttr attr);
  void setRank(uint64_t attrValue);
  void setDimSizesAttr(::mlir::DenseI64ArrayAttr attr);
  void setDimSizes(::llvm::ArrayRef<int64_t> attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::StringAttr sym_name, ::mlir::IntegerAttr rank, ::mlir::DenseI64ArrayAttr dim_sizes);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::StringAttr sym_name, ::mlir::IntegerAttr rank, ::mlir::DenseI64ArrayAttr dim_sizes);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::llvm::StringRef sym_name, uint64_t rank, ::llvm::ArrayRef<int64_t> dim_sizes = {});
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef sym_name, uint64_t rank, ::llvm::ArrayRef<int64_t> dim_sizes = {});
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static void populateDefaultProperties(::mlir::OperationName opName, Properties &properties);
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 3 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    assert(name.isRegistered() && "Operation isn't registered, missing a "
          "dependent dialect loading?");
    return name.getAttributeNames()[index];
  }

public:
  // The `dim_sizes` attribute may have size less than the rank of the mesh.
  // Returns the shape of the mesh with missing trailing dimensions
  // explicitly set as dynamic.
  ::mlir::SmallVector<int64_t> canonicalDimSizes();

  template <typename OutIt>
  void canonicalDimSizes(OutIt outIt) {
    std::copy(getDimSizes().begin(), getDimSizes().end(), outIt);
    std::fill_n(outIt, getRank() - getDimSizes().size(), 0);
  }
};
} // namespace mesh
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::mesh::ClusterOp)

namespace mlir {
namespace mesh {

//===----------------------------------------------------------------------===//
// ::mlir::mesh::ReduceScatterOp declarations
//===----------------------------------------------------------------------===//

namespace detail {
class ReduceScatterOpGenericAdaptorBase {
public:
  struct Properties {
    using meshTy = ::mlir::FlatSymbolRefAttr;
    meshTy mesh;

    auto getMesh() {
      auto &propStorage = this->mesh;
      return ::llvm::cast<::mlir::FlatSymbolRefAttr>(propStorage);
    }
    void setMesh(const ::mlir::FlatSymbolRefAttr &propValue) {
      this->mesh = propValue;
    }
    using mesh_axesTy = ::mlir::DenseI16ArrayAttr;
    mesh_axesTy mesh_axes;

    auto getMeshAxes() {
      auto &propStorage = this->mesh_axes;
      return ::llvm::dyn_cast_or_null<::mlir::DenseI16ArrayAttr>(propStorage);
    }
    void setMeshAxes(const ::mlir::DenseI16ArrayAttr &propValue) {
      this->mesh_axes = propValue;
    }
    using reductionTy = ::mlir::mesh::PartialAttr;
    reductionTy reduction;

    auto getReduction() {
      auto &propStorage = this->reduction;
      return ::llvm::dyn_cast_or_null<::mlir::mesh::PartialAttr>(propStorage);
    }
    void setReduction(const ::mlir::mesh::PartialAttr &propValue) {
      this->reduction = propValue;
    }
    using scatter_axisTy = ::mlir::IntegerAttr;
    scatter_axisTy scatter_axis;

    auto getScatterAxis() {
      auto &propStorage = this->scatter_axis;
      return ::llvm::cast<::mlir::IntegerAttr>(propStorage);
    }
    void setScatterAxis(const ::mlir::IntegerAttr &propValue) {
      this->scatter_axis = propValue;
    }
    bool operator==(const Properties &rhs) const {
      return 
        rhs.mesh == this->mesh &&
        rhs.mesh_axes == this->mesh_axes &&
        rhs.reduction == this->reduction &&
        rhs.scatter_axis == this->scatter_axis &&
        true;
    }
    bool operator!=(const Properties &rhs) const {
      return !(*this == rhs);
    }
  };
protected:
  ::mlir::DictionaryAttr odsAttrs;
  ::std::optional<::mlir::OperationName> odsOpName;
  Properties properties;
  ::mlir::RegionRange odsRegions;
public:
  ReduceScatterOpGenericAdaptorBase(::mlir::DictionaryAttr attrs = nullptr, const Properties &properties = {}, ::mlir::RegionRange regions = {});

  ReduceScatterOpGenericAdaptorBase(ReduceScatterOp op);

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize);
  const Properties &getProperties() {
    return properties;
  }

  ::mlir::DictionaryAttr getAttributes();
  ::mlir::FlatSymbolRefAttr getMeshAttr();
  ::llvm::StringRef getMesh();
  ::mlir::DenseI16ArrayAttr getMeshAxesAttr();
  ::llvm::ArrayRef<int16_t> getMeshAxes();
  ::mlir::mesh::PartialAttr getReductionAttr();
  ::mlir::mesh::Partial getReduction();
  ::mlir::IntegerAttr getScatterAxisAttr();
  ::llvm::APInt getScatterAxis();
};
} // namespace detail
template <typename RangeT>
class ReduceScatterOpGenericAdaptor : public detail::ReduceScatterOpGenericAdaptorBase {
  using ValueT = ::llvm::detail::ValueOfRange<RangeT>;
  using Base = detail::ReduceScatterOpGenericAdaptorBase;
public:
  ReduceScatterOpGenericAdaptor(RangeT values, ::mlir::DictionaryAttr attrs = nullptr, const Properties &properties = {}, ::mlir::RegionRange regions = {}) : Base(attrs, properties, regions), odsOperands(values) {}

  ReduceScatterOpGenericAdaptor(RangeT values, ::mlir::DictionaryAttr attrs, ::mlir::OpaqueProperties properties, ::mlir::RegionRange regions = {}) : ReduceScatterOpGenericAdaptor(values, attrs, (properties ? *properties.as<Properties *>() : Properties{}), regions) {}

  template <typename LateInst = ReduceScatterOp, typename = std::enable_if_t<std::is_same_v<LateInst, ReduceScatterOp>>>
  ReduceScatterOpGenericAdaptor(RangeT values, LateInst op) : Base(op), odsOperands(values) {}

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index) {
    return Base::getODSOperandIndexAndLength(index, odsOperands.size());
  }

  RangeT getODSOperands(unsigned index) {
    auto valueRange = getODSOperandIndexAndLength(index);
    return {std::next(odsOperands.begin(), valueRange.first),
             std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
  }

  ValueT getInput() {
    return (*getODSOperands(0).begin());
  }

  RangeT getOperands() {
    return odsOperands;
  }

private:
  RangeT odsOperands;
};
class ReduceScatterOpAdaptor : public ReduceScatterOpGenericAdaptor<::mlir::ValueRange> {
public:
  using ReduceScatterOpGenericAdaptor::ReduceScatterOpGenericAdaptor;
  ReduceScatterOpAdaptor(ReduceScatterOp op);

  ::mlir::LogicalResult verify(::mlir::Location loc);
};
class ReduceScatterOp : public ::mlir::Op<ReduceScatterOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::RankedTensorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::OpInvariants, ::mlir::BytecodeOpInterface::Trait, ::mlir::OpTrait::SameOperandsAndResultRank, ::mlir::SymbolUserOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = ReduceScatterOpAdaptor;
  template <typename RangeT>
  using GenericAdaptor = ReduceScatterOpGenericAdaptor<RangeT>;
  using FoldAdaptor = GenericAdaptor<::llvm::ArrayRef<::mlir::Attribute>>;
  using Properties = FoldAdaptor::Properties;
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("mesh"), ::llvm::StringRef("mesh_axes"), ::llvm::StringRef("reduction"), ::llvm::StringRef("scatter_axis")};
    return ::llvm::ArrayRef(attrNames);
  }

  ::mlir::StringAttr getMeshAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getMeshAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getMeshAxesAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getMeshAxesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getReductionAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getReductionAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr getScatterAxisAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getScatterAxisAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("mesh.reduce_scatter");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::TensorType> getInput();
  ::mlir::OpOperand &getInputMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::RankedTensorType> getResult();
  static ::mlir::LogicalResult setPropertiesFromAttr(Properties &prop, ::mlir::Attribute attr, ::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError);
  static ::mlir::Attribute getPropertiesAsAttr(::mlir::MLIRContext *ctx, const Properties &prop);
  static llvm::hash_code computePropertiesHash(const Properties &prop);
  static std::optional<mlir::Attribute> getInherentAttr(::mlir::MLIRContext *ctx, const Properties &prop, llvm::StringRef name);
  static void setInherentAttr(Properties &prop, llvm::StringRef name, mlir::Attribute value);
  static void populateInherentAttrs(::mlir::MLIRContext *ctx, const Properties &prop, ::mlir::NamedAttrList &attrs);
  static ::mlir::LogicalResult verifyInherentAttrs(::mlir::OperationName opName, ::mlir::NamedAttrList &attrs, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError);
  static ::mlir::LogicalResult readProperties(::mlir::DialectBytecodeReader &reader, ::mlir::OperationState &state);
  void writeProperties(::mlir::DialectBytecodeWriter &writer);
  ::mlir::FlatSymbolRefAttr getMeshAttr();
  ::llvm::StringRef getMesh();
  ::mlir::DenseI16ArrayAttr getMeshAxesAttr();
  ::llvm::ArrayRef<int16_t> getMeshAxes();
  ::mlir::mesh::PartialAttr getReductionAttr();
  ::mlir::mesh::Partial getReduction();
  ::mlir::IntegerAttr getScatterAxisAttr();
  ::llvm::APInt getScatterAxis();
  void setMeshAttr(::mlir::FlatSymbolRefAttr attr);
  void setMesh(::llvm::StringRef attrValue);
  void setMeshAxesAttr(::mlir::DenseI16ArrayAttr attr);
  void setMeshAxes(::llvm::ArrayRef<int16_t> attrValue);
  void setReductionAttr(::mlir::mesh::PartialAttr attr);
  void setReduction(::mlir::mesh::Partial attrValue);
  void setScatterAxisAttr(::mlir::IntegerAttr attr);
  void setScatterAxis(::llvm::APInt attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::mesh::PartialAttr reduction, ::mlir::IntegerAttr scatter_axis);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::FlatSymbolRefAttr mesh, ::mlir::DenseI16ArrayAttr mesh_axes, ::mlir::Value input, ::mlir::mesh::PartialAttr reduction, ::mlir::IntegerAttr scatter_axis);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::mlir::mesh::Partial reduction, ::llvm::APInt scatter_axis);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef mesh, ::llvm::ArrayRef<int16_t> mesh_axes, ::mlir::Value input, ::mlir::mesh::Partial reduction, ::llvm::APInt scatter_axis);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static void populateDefaultProperties(::mlir::OperationName opName, Properties &properties);
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  static void getCanonicalizationPatterns(::mlir::RewritePatternSet &results, ::mlir::MLIRContext *context);
  ::mlir::LogicalResult verifySymbolUses(::mlir::SymbolTableCollection &symbolTable);
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 4 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    assert(name.isRegistered() && "Operation isn't registered, missing a "
          "dependent dialect loading?");
    return name.getAttributeNames()[index];
  }

public:
};
} // namespace mesh
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::mesh::ReduceScatterOp)

namespace mlir {
namespace mesh {

//===----------------------------------------------------------------------===//
// ::mlir::mesh::ShardOp declarations
//===----------------------------------------------------------------------===//

namespace detail {
class ShardOpGenericAdaptorBase {
public:
  struct Properties {
    using annotate_for_usersTy = ::mlir::UnitAttr;
    annotate_for_usersTy annotate_for_users;

    auto getAnnotateForUsers() {
      auto &propStorage = this->annotate_for_users;
      return ::llvm::dyn_cast_or_null<::mlir::UnitAttr>(propStorage);
    }
    void setAnnotateForUsers(const ::mlir::UnitAttr &propValue) {
      this->annotate_for_users = propValue;
    }
    using shardTy = ::mlir::mesh::MeshShardingAttr;
    shardTy shard;

    auto getShard() {
      auto &propStorage = this->shard;
      return ::llvm::cast<::mlir::mesh::MeshShardingAttr>(propStorage);
    }
    void setShard(const ::mlir::mesh::MeshShardingAttr &propValue) {
      this->shard = propValue;
    }
    bool operator==(const Properties &rhs) const {
      return 
        rhs.annotate_for_users == this->annotate_for_users &&
        rhs.shard == this->shard &&
        true;
    }
    bool operator!=(const Properties &rhs) const {
      return !(*this == rhs);
    }
  };
protected:
  ::mlir::DictionaryAttr odsAttrs;
  ::std::optional<::mlir::OperationName> odsOpName;
  Properties properties;
  ::mlir::RegionRange odsRegions;
public:
  ShardOpGenericAdaptorBase(::mlir::DictionaryAttr attrs = nullptr, const Properties &properties = {}, ::mlir::RegionRange regions = {});

  ShardOpGenericAdaptorBase(ShardOp op);

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize);
  const Properties &getProperties() {
    return properties;
  }

  ::mlir::DictionaryAttr getAttributes();
  ::mlir::mesh::MeshShardingAttr getShardAttr();
  ::mlir::mesh::MeshShardingAttr getShard();
  ::mlir::UnitAttr getAnnotateForUsersAttr();
  bool getAnnotateForUsers();
};
} // namespace detail
template <typename RangeT>
class ShardOpGenericAdaptor : public detail::ShardOpGenericAdaptorBase {
  using ValueT = ::llvm::detail::ValueOfRange<RangeT>;
  using Base = detail::ShardOpGenericAdaptorBase;
public:
  ShardOpGenericAdaptor(RangeT values, ::mlir::DictionaryAttr attrs = nullptr, const Properties &properties = {}, ::mlir::RegionRange regions = {}) : Base(attrs, properties, regions), odsOperands(values) {}

  ShardOpGenericAdaptor(RangeT values, ::mlir::DictionaryAttr attrs, ::mlir::OpaqueProperties properties, ::mlir::RegionRange regions = {}) : ShardOpGenericAdaptor(values, attrs, (properties ? *properties.as<Properties *>() : Properties{}), regions) {}

  template <typename LateInst = ShardOp, typename = std::enable_if_t<std::is_same_v<LateInst, ShardOp>>>
  ShardOpGenericAdaptor(RangeT values, LateInst op) : Base(op), odsOperands(values) {}

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index) {
    return Base::getODSOperandIndexAndLength(index, odsOperands.size());
  }

  RangeT getODSOperands(unsigned index) {
    auto valueRange = getODSOperandIndexAndLength(index);
    return {std::next(odsOperands.begin(), valueRange.first),
             std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
  }

  ValueT getSrc() {
    return (*getODSOperands(0).begin());
  }

  RangeT getOperands() {
    return odsOperands;
  }

private:
  RangeT odsOperands;
};
class ShardOpAdaptor : public ShardOpGenericAdaptor<::mlir::ValueRange> {
public:
  using ShardOpGenericAdaptor::ShardOpGenericAdaptor;
  ShardOpAdaptor(ShardOp op);

  ::mlir::LogicalResult verify(::mlir::Location loc);
};
class ShardOp : public ::mlir::Op<ShardOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::RankedTensorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::OpInvariants, ::mlir::BytecodeOpInterface::Trait, ::mlir::ConditionallySpeculatable::Trait, ::mlir::OpTrait::AlwaysSpeculatableImplTrait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::OpTrait::SameOperandsAndResultType, ::mlir::InferTypeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = ShardOpAdaptor;
  template <typename RangeT>
  using GenericAdaptor = ShardOpGenericAdaptor<RangeT>;
  using FoldAdaptor = GenericAdaptor<::llvm::ArrayRef<::mlir::Attribute>>;
  using Properties = FoldAdaptor::Properties;
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("annotate_for_users"), ::llvm::StringRef("shard")};
    return ::llvm::ArrayRef(attrNames);
  }

  ::mlir::StringAttr getAnnotateForUsersAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getAnnotateForUsersAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getShardAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getShardAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("mesh.shard");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::RankedTensorType> getSrc();
  ::mlir::OpOperand &getSrcMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::RankedTensorType> getResult();
  static ::mlir::LogicalResult setPropertiesFromAttr(Properties &prop, ::mlir::Attribute attr, ::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError);
  static ::mlir::Attribute getPropertiesAsAttr(::mlir::MLIRContext *ctx, const Properties &prop);
  static llvm::hash_code computePropertiesHash(const Properties &prop);
  static std::optional<mlir::Attribute> getInherentAttr(::mlir::MLIRContext *ctx, const Properties &prop, llvm::StringRef name);
  static void setInherentAttr(Properties &prop, llvm::StringRef name, mlir::Attribute value);
  static void populateInherentAttrs(::mlir::MLIRContext *ctx, const Properties &prop, ::mlir::NamedAttrList &attrs);
  static ::mlir::LogicalResult verifyInherentAttrs(::mlir::OperationName opName, ::mlir::NamedAttrList &attrs, llvm::function_ref<::mlir::InFlightDiagnostic()> emitError);
  static ::mlir::LogicalResult readProperties(::mlir::DialectBytecodeReader &reader, ::mlir::OperationState &state);
  void writeProperties(::mlir::DialectBytecodeWriter &writer);
  ::mlir::mesh::MeshShardingAttr getShardAttr();
  ::mlir::mesh::MeshShardingAttr getShard();
  ::mlir::UnitAttr getAnnotateForUsersAttr();
  bool getAnnotateForUsers();
  void setShardAttr(::mlir::mesh::MeshShardingAttr attr);
  void setAnnotateForUsersAttr(::mlir::UnitAttr attr);
  void setAnnotateForUsers(bool attrValue);
  ::mlir::Attribute removeAnnotateForUsersAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value src, ::mlir::mesh::MeshShardingAttr shard, /*optional*/::mlir::UnitAttr annotate_for_users);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value src, ::mlir::mesh::MeshShardingAttr shard, /*optional*/::mlir::UnitAttr annotate_for_users);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value src, ::mlir::mesh::MeshShardingAttr shard, /*optional*/::mlir::UnitAttr annotate_for_users);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value src, ::mlir::mesh::MeshShardingAttr shard, /*optional*/bool annotate_for_users = false);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value src, ::mlir::mesh::MeshShardingAttr shard, /*optional*/bool annotate_for_users = false);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value src, ::mlir::mesh::MeshShardingAttr shard, /*optional*/bool annotate_for_users = false);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  static ::mlir::LogicalResult inferReturnTypes(::mlir::MLIRContext *context, ::std::optional<::mlir::Location> location, ::mlir::ValueRange operands, ::mlir::DictionaryAttr attributes, ::mlir::OpaqueProperties properties, ::mlir::RegionRange regions, ::llvm::SmallVectorImpl<::mlir::Type>&inferredReturnTypes);
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 2 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    assert(name.isRegistered() && "Operation isn't registered, missing a "
          "dependent dialect loading?");
    return name.getAttributeNames()[index];
  }

public:
};
} // namespace mesh
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::mesh::ShardOp)


#endif  // GET_OP_CLASSES

